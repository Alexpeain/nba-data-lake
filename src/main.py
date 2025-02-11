import boto3
import json
import requests
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
region_name = os.getenv("AWS_REGION")
sport_api_key = os.getenv("NBA_API_KEY")
bucket_name = os.getenv("BUCKET_NAME")
glue_database_name = "glue_nba_datalake"
athena_output_location = f"s3://{bucket_name}/athena-results/"

# Create AWS clients
s3_client = boto3.client("s3", region_name=region_name)
glue_client = boto3.client("glue", region_name=region_name)
athena_client = boto3.client("athena", region_name=region_name)

def create_s3_bucket():
    """Create an S3 bucket."""
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region_name
            }
        )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            print(f"S3 bucket '{bucket_name}' already exists and is owned by you.")
        else:
            print(f"Error creating S3 bucket: {e}")

def fetch_nba_data():
    """Fetch NBA player data from sportsdata.io."""
    try:
        nba_endpoint = "https://api.sportsdata.io/v3/nba/scores/json/Players"
        headers = {"Ocp-Apim-Subscription-Key": sport_api_key}

        response = requests.get(nba_endpoint, headers=headers)
        response.raise_for_status()
        print("Fetched NBA data successfully.")

        return response.json()
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []

def upload_to_s3(data, file_name):
    """Upload NBA player data to S3."""
    if not data:
        print("No data to upload.")
        return

    file_path = f"raw-data/{file_name}"

    s3_client.put_object(Bucket=bucket_name,
                         Key=file_path,
                         Body=json.dumps(data),
                         ContentType="application/json")
    print(f"Uploaded file to S3: {file_path}")

def create_glue_database(database_name):
    """Create a Glue database if it does not exist."""
    try:
        glue_client.create_database(DatabaseInput={"Name": database_name})
        print(f"Glue database '{database_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating Glue database: {e}")

def create_glue_table(database_name, table_name, columns):
    try:
        glue_client.create_table(
            DatabaseName=database_name,
            TableInput={
                "Name": table_name,
                "StorageDescriptor": {
                    "Columns": columns,
                    "Location": f"s3://{bucket_name}/raw-data/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print(f"Glue table '{table_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating Glue table: {e}")

def query_athena(database_name, query):
    try:
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database_name},
            ResultConfiguration={"OutputLocation": athena_output_location}
        )
        print("Athena query started successfully.")
        return response
    except ClientError as e:
        print(f"Error starting Athena query: {e}")

# Main execution
create_s3_bucket()
nba_data = fetch_nba_data()
if nba_data:
    upload_to_s3(nba_data, "nba_players.json")
    create_glue_database(glue_database_name)
    create_glue_table(glue_database_name, "nba_players", [
        {"Name": "PlayerID", "Type": "int"},
        {"Name": "FirstName", "Type": "string"},
        {"Name": "LastName", "Type": "string"},
        {"Name": "Team", "Type": "string"},
        {"Name": "Position", "Type": "string"},
        {"Name": "Points", "Type": "int"}
    ])