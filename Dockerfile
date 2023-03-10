FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

RUN mkdir -p /opt/prefect/data
RUN mkdir -p /opt/prefect/flows

COPY etl/web_to_gcs_etl.py /opt/prefect/flows
COPY etl/data /opt/prefect/data

