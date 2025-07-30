# 🛠️ AWS Serverless ETL Pipeline for E-Commerce Order Data

This project demonstrates a complete **end-to-end serverless ETL (Extract, Transform, Load) pipeline** built on AWS. It processes incoming JSON order data, flattens nested structures, converts it into Parquet format, and stores it in a data lake for analysis using Amazon Athena.

---

##  Architecture Overview

      +-------------+
      | JSON Orders |
      |   (S3)      |
      +------+------+        
             |
    [Trigger: S3 Event]
             ↓
    +------------------+
    | AWS Lambda       |
    | - Flattens JSON  |
    | - Converts to    |
    |   Parquet        |
    +--------+---------+
             |
             ↓
    +---------------------+
    | S3 Data Lake        |
    | (Parquet format)    |
    +--------+------------+
             |
    +---------------------+
    | AWS Glue Crawler    |
    | - Scans Data Lake   |
    | - Updates Catalog   |
    +--------+------------+
             |
    +---------------------+
    | Amazon Athena       |
    | - SQL on Parquet    |
    +---------------------+

---

##  Key Features

-  **Data Ingestion**: JSON order data uploaded to an S3 bucket.
- ⚙ **Serverless ETL with AWS Lambda**: 
  - Flattens nested customer and product data.
  - Converts JSON to efficient columnar **Parquet** format.
-  **Data Lake Storage**: Transformed data stored in a separate S3 location.
-  **AWS Glue Crawler**: Scans parquet files and catalogs schema.
-  **Athena Integration**: Query-ready data via SQL interface.

---

##  Technologies Used

| Service                                  | Purpose                                             |
|------------------------------------------|-----------------------------------------------------|
| **AWS S3**                               | Stores raw JSON and processed Parquet data.         |
| **AWS Lambda**                           | Executes transformation logic on trigger.           |
| **AWS Glue**                             | Crawls data and maintains metadata catalog.         |
| **Amazon Athena** 		           | SQL querying over S3 Data Lake.                     |
| **Python (pandas, datetime, boto3, io)** | Data wrangling and parquet conversion.              |

---


---

##  Setup & Usage

> ⚠ This project assumes your AWS infrastructure is already configured (S3, Lambda, IAM Roles, Glue, Athena).

### 1. Upload Raw JSON to S3
Upload JSON order data into the source S3 bucket (e.g. `orders-input-bucket/`).

### 2. Lambda Function Execution
Lambda gets automatically triggered via S3 event:
- Flattens and transforms nested data
- Converts to `.parquet`
- Stores result into target S3 bucket (`orders_parquet_datalake/`)

### 3. Glue Crawler
Run the AWS Glue Crawler:
- Scans new Parquet files
- Updates AWS Glue Data Catalog

### 4. Athena Querying
Use SQL queries in Athena:
```sql
SELECT * FROM orders_catalog.orders_data LIMIT 10;




