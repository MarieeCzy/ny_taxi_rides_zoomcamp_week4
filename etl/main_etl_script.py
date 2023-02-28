from prefect import flow
from prefect.task_runners import SequentialTaskRunner
from gcs_to_bq_etl import etl_gcs_to_bq
from web_to_gcs_etl import etl_web_to_gcs

@flow (log_prints=True, retries=3, task_runner=SequentialTaskRunner())
def etl_main_flow(months: list = [1,2,3,4],
                  year: int = 2021,
                  colors: list = ['yellow', 'green']
                  ) -> None:
    '''
    The main flow function accepting arguments describing datasets and 
    calling the subflow function etl_web_to_gcs and with SequentialTaskRunner etl_gcs_to_bq. 
    
    Args:
        months (list): The months the data comes from
        year (int): The year the data comes from
        colors (list): The collections from which the data comes
    
    Notes:
        See: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page for more info.
        Data from official page available in .parquet format.
    '''
    for color in colors:
        for month in months:
            etl_web_to_gcs(year, month, color)
            etl_gcs_to_bq(year, month, color)
    

if __name__ == "__main__":
    months = [1,2,3,4,5]
    year = 2021
    color = ['yellow', 'green']
    etl_main_flow(months, year, color)