from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@flow 
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    print(year, month, color)

@flow (log_prints=True, retries=3)
def etl_main_flow(months: list = [1,2,3,4],
                  year: int = 2021,
                  colors: list = ['yellow', 'green']
                  ) -> None:
    '''
    The main flow function accepting arguments describing datasets and 
    calling the subflow function etl_web_to_gcs.
    
    Args:
        months (list): The months the data comes from
        year (int): The year the data comes from
        color (list): The collection from which the data comes
    
    Notes:
        See: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page for more info.
    '''
    for color in colors:
        for month in months:
            etl_web_to_gcs(year, month, color)
    
    
if __name__ == "__main__":
    months = [1,2,3,4,5]
    year = 2021
    color = ['yellow', 'green']
    etl_main_flow(months, year, color)