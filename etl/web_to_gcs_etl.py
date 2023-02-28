from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect.task_runners import SequentialTaskRunner
from gcs_to_bq_etl import etl_gcs_to_bq


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch_data(dataset_url: str) -> pd.DataFrame:
    '''
    Read taxi data from web into pandas DataFrame.
    
    Args:
        dataset_url (str): Url source of data
        
    Notes:
        Backup taxi data files in .csv format: 
        https://github.com/DataTalksClub/nyc-tlc-data
    '''
    df = pd.read_csv(dataset_url)
    return df

@task
def pre_clean_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Fix some dtype issues.
    
    Args: 
        df (pd.Dataframe): Raw taxi dataframe downloaded from web.
    '''
    try:
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        try:
            df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
            df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
        
        except KeyError:
            pass
    except KeyError:
        pass
    return df


@task
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    '''
    Write pre cleaned Data Frame locally as .parquet file.
    
    Args:
        df (pd. DataFrame): Pre cleaned DataFrame
        color (str): The collection from which the data comes
        dataset_file (str): Name of .parquet file
    '''
    
    path = Path(f'data/{dataset_file}.parquet')
    df.to_parquet(path, compression='gzip')
    return path


@task
def write_to_gcs(path: Path) -> None:
    '''
    Uploading local parquet file to Google Cloud Storage bucket.
    
    Args:
        path (Path): URL path to .parquet taxi dataset saved locally in /data directory.
    '''
    gcp_cloud_storage_bucket_block = GcsBucket.load("dbt-gcs-bucket")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)

@flow
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    '''
    The main sub-flow function managing the tasks of:
    - downloading datasets, 
    - pre-cleaning,
    - local saving,
    - loading to Google Cloud Storage.
    
    Args:
        year (int): The year the data comes from
        month (int): The month the data comes from
        color (str): The collection from which the data comes
    '''
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz'
    
    df = fetch_data(dataset_url)
    clean_df = pre_clean_df(df)
    local_path = write_local(clean_df, color, dataset_file)
    write_to_gcs(local_path)