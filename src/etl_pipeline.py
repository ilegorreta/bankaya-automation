#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
# import snowflake.connector
# from snowflake.connector.pandas_tools import write_pandas

def get_postgres_connection(database, host, user, password, port):
    connection = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)
    return connection

def main():
    # Connect to DB
    # conn = snowflake.connector.connect(
    #     user = os.getenv("SNOWFLAKE_USER"),
    #     password = os.getenv("SNOWFLAKE_PASSWORD"),
    #     account = os.getenv("SNOWFLAKE_ACCOUNT"),
    #     warehouse = os.getenv("SNOWFLAKE_WAREHOUSE"),
    #     )
    # conn.cursor().execute('USE ROLE SYSADMIN')
    # conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS test_warehouse")
    # conn.cursor().execute("USE WAREHOUSE test_warehouse")
    # conn.cursor().execute("CREATE DATABASE IF NOT EXISTS bankaya_db")
    # conn.cursor().execute("USE DATABASE bankaya_db")
    # conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS test_schema")
    # conn.cursor().execute("USE SCHEMA test_schema")

    try:
        host = os.getenv("RDS_HOST")
        user = os.getenv("RDS_USER")
        password = os.getenv("RDS_PASSWORD")
        db = os.getenv("RDS_DB")
        port = os.getenv("RDS_PORT")
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        tables = ['customer', 'item', 'orders']
        # Connect to PostgreSQL server
        dbConnection = engine.connect()
        for table in tables:
            df = pd.read_sql(f"select * from {table}", dbConnection)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()