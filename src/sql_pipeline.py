#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os

TABLE_NAMES = ['customer', 'item', 'orders']

def table_definitons():
    """Create table definitons for the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS customer(
        customer_id SERIAL PRIMARY KEY,
        first_name VARCHAR(64) NOT NULL,
        last_name VARCHAR(64) NOT NULL,
        phone_number INTEGER NOT NULL,
        curp VARCHAR(18) NOT NULL,
        rfc VARCHAR(13) NOT NULL,
        address TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS item(
            item_id SERIAL PRIMARY KEY,
            name VARCHAR(64) NOT NULL,
            price FLOAT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders(
            order_id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customer (customer_id),
            item_id INTEGER NOT NULL REFERENCES item (item_id),
            order_date DATE NOT NULL DEFAULT CURRENT_DATE,
            price FLOAT NOT NULL,
            comments TEXT
        )
        """
    ]
    return commands

def get_postgres_connection(database, host, user, password, port):
    connection = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)
    return connection

def main():
    """Create tables (if not exist) in Postgres RDS Instance and insert data based on CSV files"""
    try:
        # Init RDS connection
        conn = get_postgres_connection(
            os.getenv("RDS_DB"), 
            os.getenv("RDS_HOST"), 
            os.getenv("RDS_USER"),
            os.getenv("RDS_PASSWORD"),
            os.getenv("RDS_PORT")
            )
        cursor = conn.cursor()
        # Get CREATE table definitions
        commands = table_definitons()
        # Execute CREATE TABLE statements
        for command in commands:
            cursor.execute(command)
        # Insert data from CSV files into RDS tables
        for table in TABLE_NAMES:
            # Read CSV files
            with open(f'data/sql/{table}.csv', 'r') as row:
                # Skip the header row
                next(row)
                # Insert data
                cursor.copy_from(row, table, sep=',')
        # Close communication with RDS
        cursor.close()
        # Commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
