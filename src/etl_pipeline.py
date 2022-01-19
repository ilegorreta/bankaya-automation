#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import psycopg2
import numpy as np
import pandas as pd
import boto3
from sqlalchemy import create_engine
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

def get_postgres_connection(database, host, user, password, port):
    connection = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)
    return connection

def build_snowflake_create_table_command(df, table):
    """Helper function to construct the string required to create Snowflake tables"""
    # String to specify the CREATE TABLE statement 
    create_table_str = f'CREATE OR REPLACE TABLE "{table}" ( '
    df_types = df.dtypes.to_dict()
    # Iterate through pandas columns data types to append to the 'CREATE TABLE' string 
    for key, val in df_types.items():
        if val == np.int64:
            val = "INTEGER"
        elif val == np.float64:
            val = "FLOAT"
        else:
            val = "STRING"
        create_table_str += f'"{key}": {val}, '
    # Remove trailing comma and white space
    create_table_str = create_table_str[:-2]
    # Close Parenthesis for the 'CREATE TABLE' statement
    create_table_str += ' )'
    return create_table_str

def rds_etl_pipeline(conn):
    """ETL pipeline to retrieve data from RDS into Pandas and then insert into Snowflake tables"""
    try:
        # Get Snowflake Credentials from environment variables
        host = os.getenv("RDS_HOST")
        user = os.getenv("RDS_USER")
        password = os.getenv("RDS_PASSWORD")
        db = os.getenv("RDS_DB")
        port = os.getenv("RDS_PORT")
        # Create engine to connect to Postgres RDS
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}", pool_recycle=3600)
        tables = ['customer', 'item', 'orders']
        for table in tables:
            # Read data from RDS table and load it as a Pandas Dataframe
            df = pd.read_sql_query(f'select * from {table}', con=engine)
            create_table_str = build_snowflake_create_table_command(df, table)
            # Execute CREATE TABLE command into Snowflake
            conn.cursor().execute(create_table_str)
            # Insert Dataframe records into Snowflake table
            write_pandas(conn, df, table_name=table)
    except Exception as e:
        print(f"ERROR: {e}")

def dynamodb_etl_pipeline(conn):
    """ETL pipeline to retrieve data from DynamoDB into Pandas and then insert into Snowflake tables"""
    try:
        TABLE_NAMES = ['customers_data', 'items_data', 'items_bought_data']
        dynamo = boto3.resource("dynamodb")
        for table_name in TABLE_NAMES:
            table = dynamo.Table(table_name)
            # Get DynamoDB data
            dynamo_data_list = table.scan()
            # Convert dynamoDB list of dictionaries into Pandas Dataframe
            df = pd.DataFrame(dynamo_data_list['Items'])
            # Add naming suffix to differenciate Snowflake tables coming from RDS from the ones coming from DynamoDB
            snowflake_table_name = table_name + '_dynamodb'
            create_table_str = build_snowflake_create_table_command(df, snowflake_table_name)
            # Execute CREATE TABLE command into Snowflake
            conn.cursor().execute(create_table_str)
            # Insert Dataframe records into Snowflake table
            write_pandas(conn, df, table_name=table)
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    """Function to extract data from RDS and DynamoDB and upload them into Snowflake"""
    try:
        # Connect to Snowflake DB
        conn = snowflake.connector.connect(
            user = os.getenv("SNOWFLAKE_USER"),
            password = os.getenv("SNOWFLAKE_PASSWORD"),
            account = os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse = os.getenv("SNOWFLAKE_WAREHOUSE"),
            )
        # Create WH, DB and Schema
        conn.cursor().execute('USE ROLE SYSADMIN')
        conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS test_warehouse")
        conn.cursor().execute("USE WAREHOUSE test_warehouse")
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS bankaya_db")
        conn.cursor().execute("USE DATABASE bankaya_db")
        conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS test_schema")
        conn.cursor().execute("USE SCHEMA test_schema")
        # Call ETL functions from each DB engine
        rds_etl_pipeline(conn)
        dynamodb_etl_pipeline(conn)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
