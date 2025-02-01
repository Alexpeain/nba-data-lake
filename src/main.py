import boto3
import json
import time
import urllib.request
from datetime import datetime,timedelta
import os 

#variable environment
region_name = os.getenv("AWS_REGION")
sport_api_key = os.getenv("NBA_API_KEY")
bucket_name = os.getenv("BUCKET_NAME")