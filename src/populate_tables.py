import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os

def main():
    try:
        host = os.getenv("RDS_HOST")
        user = os.getenv("RDS_USER")
        password = os.getenv("RDS_PASSWORD")
        db = os.getenv("RDS_DB")
        port = os.getenv("RDS_PORT")
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        tables = ['customer', 'item', 'orders']
        for table in tables:
            df = pd.read_csv(f"data/{table}.csv")
            df.to_sql(con= engine, name=table, if_exists="replace")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
