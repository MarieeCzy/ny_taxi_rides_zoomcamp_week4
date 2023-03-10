from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.credentials import GcpCredentials

bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("zoom-gcp-creds"),
    bucket="dbt-bucket-de-zoomcamp",  # insert your  GCS bucket name
)

bucket_block.save("dbt-gcs-bucket", overwrite=True)