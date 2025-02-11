import os
from unittest.mock import patch # For mocking environment variables
import pytest # Import pytest
from main import fetch_nba_data, create_s3_bucket, create_glue_database, create_glue_table, query_athena

# Mock environment variables (Do this before importing boto3 in main.py)
@pytest.fixture(autouse=True)
def mock_env_variables():
    with patch.dict(os.environ, {
        "AWS_REGION": "test_region",
        "NBA_API_KEY": "test_api_key",
        "BUCKET_NAME": "test_bucket",
    }):
        yield # Important! This allows the test to run with the mocked variables

def test_fetch_nba_data(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"PlayerID": 1, "FirstName": "Test"}]  # Mock the API response

    mocker.patch("main.requests.get", return_value=mock_response)  # Mock requests.get

    data = fetch_nba_data()
    assert isinstance(data, list)
    assert data[0]["PlayerID"] == 1
    print("fetch_nba_data passed")

def test_create_s3_bucket(mocker):
    mock_s3_client = mocker.Mock()
    mocker.patch("main.s3_client", mock_s3_client)  # Mock the s3_client

    create_s3_bucket()

    mock_s3_client.head_bucket.assert_called_once_with(Bucket="test_bucket")
    print("create_s3_bucket passed")

def test_create_glue_database(mocker):
    mock_glue_client = mocker.Mock()
    mocker.patch("main.glue_client", mock_glue_client)

    create_glue_database("test_database")

    mock_glue_client.create_database.assert_called_once_with(DatabaseInput={"Name": "test_database"})
    print("create_glue_database passed")

def test_create_glue_table(mocker):
    mock_glue_client = mocker.Mock()
    mocker.patch("main.glue_client", mock_glue_client)

    columns = [
        {"Name": "PlayerID", "Type": "int"},
        # ... other columns
    ]
    create_glue_table("test_database", "test_table", columns)

    mock_glue_client.create_table.assert_called_once()  # Check that create_table was called
    # You could add more specific checks for the arguments passed to create_table if needed
    print("create_glue_table passed")

def test_query_athena(mocker):
    mock_athena_client = mocker.Mock()
    mocker.patch("main.athena_client", mock_athena_client)

    response = query_athena("test_database", "SELECT * FROM test_table")

    mock_athena_client.start_query_execution.assert_called_once()  # Check that query execution was started
    print("query_athena passed")