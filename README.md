# NBA Data Lake with AWS Services: AWS S3, AWS Glue, AWS Athena

## Description
This project sets up a data lake for NBA data using AWS services such as S3, Glue, and Athena. It fetches NBA player data from an external API, stores it in an S3 bucket, and uses Glue to create a database and table for querying the data with Athena.

## Prerequisites
1. Clone the repository:
    ```bash
    git clone https://github.com/Alexpeain/nba-data-lake.git
    cd nba-data-lake
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the following:
    - Python 3.x
    - AWS Account
    - AWS CLI configured with necessary permissions (IAM roles/users for S3, Glue, Athena)

## Environment Variables
1. Create a [.env](http://_vscodecontentref_/2) file and add it to [.gitignore](http://_vscodecontentref_/3):
    ```bash
    echo .env >> .gitignore
    ```

2. Add the following environment variables  theto [.env](http://_vscodecontentref_/4) file:
    ```bash
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_REGION=your_aws_region
    NBA_API_KEY=your_api_key_here
    BUCKET_NAME=your_bucket_name
    GLUE_DATABASE_NAME=glue_nba_datalake
    ATHENA_OUTPUT_LOCATION=s3://your_bucket_name/athena-results/
    ```

## Steps to Run
1. Ensure your AWS CLI is configured with the necessary permissions:
    ```bash
    aws configure
    ```

2. Run the main script:
    ```bash
    python src/main.py
    ```
3. Test the main script:
    ```bash
    python src/test.py
    ```
    
## Project Structure

nba-data-lake/ 
├── src/     
|   ├── main.py 
|   │── test.py 
├── .env 
├── .gitignore 
├── README.md 
└── requirements.txt

## Additional Information
- **AWS S3**: Used to store raw NBA data.
- **AWS Glue**: Used to create a database and table for the NBA data.
- **AWS Athena**: Used to query the NBA data stored in S3.


# License
This project is licensed under the MIT License.