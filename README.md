# Bankaya DE Test - ETL Automation
 
This application automates an ETL process, making use of Relational and Non-Relational databases, as well as a Data Warehouse.

The goal of this application is to integrate several technologies using Python and to show the execution of a small data-driven ETL pipeline, which based on a set of local data files (CSV and JSON), inserts the data into the corresponding database engine, creating relational tables on an Amazon RDS (for PostgreSQL) instance for the CSV files, and non-relational DynamoDB tables for the JSON files.

The whole project was developed through GitHub Actions, which is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate the development, testing, and deployment of the application throughout its lifecyle. This way we can deploy our application using GitHub's servers based on a version control system.

Moreover, the database infrastructure was built upon Terraform, an open-source infrastructure as code software tool which let you create cloud resources across several Cloud Service Providers (CSP). For this application, the chosen public cloud was Amazon Web Services (AWS). Throughout the development of the application, Terraform Cloud was integrated with GitHub Actions to provision infrastructure securely and reliably in the cloud with free remote state storage, offering remote terraform execution and version control integration.

The following list shows the AWS resources provisioned through Terraform:

* **Amazon RDS for PostgreSQL**: Relational DB in the AWS Cloud
* **DynamoDB**: NoSQL DB in the AWS Cloud

Regarding the final destination of the data uploaded into both databases, this application used Snowflake as a Data Warehouse to store the data coming from both previous sources. It is worth to mention that initially Amazon Redshift was planned as the Data Warehousing platform, although this service is not part of the AWS Free-Tier, so it was discarted over Snowflake, even though it is not free either, that's why the Data Warehouse modules were just simulated (the code is written and should be work as expected, although was not tested on actual Snowflake instance).

Additionally, it is noteworthy going through the directory structure:

```
.
├── Dockerfile : (For VS Code Dev container testing purposes)
├── README.md
├── data : (Directory containing data that is going to be inserted into remote databases)
│   ├── nosql
│   │   ├── customer.json
│   │   ├── item.json
│   │   └── orders.json
│   └── sql
│       ├── customer.csv
│       ├── item.csv
│       └── orders.csv
├── deploy : (Terraform related files)
│   ├── dynamodb.tf
│   ├── main.tf
│   ├── rds.tf
│   └── variables.tf
├── requirements.txt : (Required dependencies for Python files)
└── src : (Python files containing the logic to move data across platforms)
    ├── etl_pipeline.py
    ├── nosql_pipeline.py
    └── sql_pipeline.py
```

Finally, it's worth to specify the triggers for the different workflows:

* **Terraform resource creation (RDS and DynamoDB)**:
  * **Terraform Plan**: Pull Request targeting ```Main``` branch
  * **Terraform Apply**: Push on ```Main``` branch
* SQL (RDS) pipeline: push on ```sql_pipeline``` branch
* NoSQL (DynamoDB) pipeline: push on ```nosql_pipeline``` branch
* ETL pipeline (RDS, DynamoDB into Snowflake): push on ```etl_pipeline``` branch

The reason why these pipelines are not sequentially triggered is due to eventual consistency, we cannot guarantee that the resources will be fully available to write on after their creation on Terraform, so the proposed implementation makes use of different branches to segment the whole pipeline.

Author: Ivan Legorreta
