from pathlib import Path
import pandas as pd
from prefect import flow,task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials



@task
def extract_from_gcs(year: int, month: int, color: str) -> Path:
    '''
    Download trip data from GCS
    '''
    gcs_url = f'data/{color}_tripdata_{year}-{month:02}.parquet'
    gcp_cloud_storage_bucket_block = GcsBucket.load("dbt-gcs-bucket")
    gcp_cloud_storage_bucket_block.get_directory(from_path=gcs_url, local_path="../data/")
    return Path(f'{gcs_url}')

@task(log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    '''
    Extract DataFrame from .parquet file
    '''
    df = pd.read_parquet(path)
    return df

@task
def write_to_bq(df: pd.DataFrame, year: int, month: int, color: str) -> None:
    '''
    Write DataFrame into BigQuery
    '''
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    destination_table = f'trips_data_all.{color}_trip_data_{year}_{month:02}'
    df.to_gbq(
        destination_table= destination_table,
        project_id= 'focus-poet-376519',
        credentials= gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists= 'append'
    )

@flow
def etl_gcs_to_bq(year: int, month: int, color: str):
    '''
    ETL subflow responsible for extracting data from Google Cloud Storage 
    and loading into Big Query.
    
    Args:
        year (int): The year the data comes from
        month (int): The month the data comes from
        color (str): The collection from which the data comes
    '''
    path = extract_from_gcs(year, month, color)
    df = transform(path)
    write_to_bq(df, year, month, color)
    
    
    