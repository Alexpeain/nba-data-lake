import boto3
import json
import time
import requests
from datetime import datetime,timedelta
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
#variable environment
region_name = os.getenv("AWS_REGION")
sport_api_key = os.getenv("NBA_API_KEY")
bucket_name = os.getenv("BUCKET_NAME")

#glue anthena

#creat aws clients 
s3_client = boto3.client("s3",region_name=region_name)
glue_client = boto3.client("glue",region_name=region_name)
athena_client = boto3.client("athena", region_name=region_name)


#create a database
def create_s3_bucket():
    """Check if S3 bucket exists, otherwise create it."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print("Bucket already exists")
    except Exception as e:
        print(f"Error: S3 bucket '{bucket_name}' does not exist or you don't have access: {e} ")

create_s3_bucket()           

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
nba_data = fetch_nba_data()

#upload data to s3
def upload_to_s3(data,file_name):
    """Upload NBA player data to S3."""
    if not data:
        print("No data to upload.")
        return
    
    file_path = f"raw/{file_name}"
    s3_client.put_object(Bucket=bucket_name,
                         Key=file_path, 
                         Body=json.dumps(data),
                         ContentType="application/json")
    print(f"Uploaded file to S3: {file_path}")

upload_to_s3(nba_data, "nba_players.json")

#Create a Glue database
def create_glue_database():
    """Create a Glue database if it does not exist."""

    try:
        glue_client.create_database(DatabaseInput={"Name": "nba_players"})
        print("Glue database nba_players created successfully.")
    except glue_client.exceptions.AlreadyExistsException:
        print("Glue database nba_players already exists.")
    except Exception as e:
        print(f"Error creating Glue database: {e}")

create_glue_database()
