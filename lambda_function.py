import json
import boto3
import pandas as pd
import io
from datetime import datetime

def flatten(data):
    order_data = []

    for order in data:
        for product in order['products']:
            row_orders = {
                'order_id': order['order_id'],
                'order_date': order['order_date'],
                'total_amount': order['total_amount'],
                'customer_id': order['customer']['customer_id'],
                'customer_name': order['customer']['name'],
                'email': order['customer']['email'],
                'address': order['customer']['address'],
                'product_id': product['product_id'],
                'product_name': product['name'],
                'category': product['category'],
                'price': product['price'],
                'quantity': product['quantity']
            }
            order_data.append(row_orders)

    df_order_data = pd.DataFrame(order_data)  
    return df_order_data
    
def lambda_handler(event, context):
    # TODO implement
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    
    #Read and parse JSON content
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
    df = flatten(data)

    # in-memory binary buffer to hold data like a file, but without writing to disc
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    key_staging=f'orders_parquet_datalake/orders_ETL_{timestamp}.parquet'
    

    s3.put_object(Bucket=bucket_name, Key=key_staging, Body=parquet_buffer.getvalue())

    crawler_name = 'etl_pipeline_crawler'
    glue = boto3.client('glue')
    response = glue.start_crawler(Name=crawler_name)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
