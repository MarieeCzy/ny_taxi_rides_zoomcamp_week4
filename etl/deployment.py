from main_etl_script import etl_main_flow
from web_to_gcs_etl import etl_web_to_gcs
from prefect.deployments import Deployment
from params import parameters
from prefect.infrastructure.docker import DockerContainer


main_deployment = Deployment.build_from_flow(
    flow=etl_main_flow,
    name="Dbt main flow",
    parameters= parameters,
    work_queue_name="default"
)

docker_block = DockerContainer.load('etl-gcs-block')

etl_web_to_gcs_deployment = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name="Etl web to GCS flow",
    parameters= {'year': 2019, 'month': 2, 'color': 'yellow'},
    infrastructure=docker_block,
    work_queue_name="default"
)

if __name__ == "__main__":
    main_deployment.apply()
    etl_web_to_gcs_deployment.apply()
    
