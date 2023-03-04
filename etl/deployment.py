from main_etl_script import etl_main_flow
from prefect.deployments import Deployment
from params import parameters


main_deployment = Deployment.build_from_flow(
    flow=etl_main_flow,
    name="Dbt main flow",
    parameters= parameters,
    work_queue_name="default"
)

if __name__ == "__main__":
    main_deployment.apply()
    
