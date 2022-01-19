#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
from decimal import Decimal

CUSTOMER_TABLE_NAME = "customers_data"
ITEM_TABLE_NAME = "items_data"
ORDERS_TABLE_NAME = "items_bought_data"

dynamo = boto3.resource("dynamodb")

CUSTOMER_TABLE = dynamo.Table(CUSTOMER_TABLE_NAME)
ITEM_TABLE = dynamo.Table(ITEM_TABLE_NAME)
ORDERS_TABLE = dynamo.Table(ORDERS_TABLE_NAME)

def main():
    nosql_files = ["customer.json", "item.json", "orders.json"]
    for file in nosql_files:
        with open(f"data/nosql/{file}") as json_file:
            data_list = json.load(json_file)
        if file == "customer.json":
            table = CUSTOMER_TABLE
        elif file == "item.json":
            table = ITEM_TABLE
        else:
            table = ORDERS_TABLE
        for record in data_list:
        # Float types are not supported by DynamoDB SDK. Should use Decimal types instead
            table.put_item(Item=json.loads(json.dumps(record), parse_float=Decimal))
    
    print("NOSQL data successfully uploaded into DynamoDB tables!")

if __name__ == "__main__":
    main()
