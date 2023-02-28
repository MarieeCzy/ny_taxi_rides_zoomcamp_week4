from main_etl_script import etl_main_flow
from prefect.deployments import Deployment

main_deployment = Deployment.build_from_flow(
    flow=etl_main_flow,
    name="Dbt main flow",
    parameters= {"months": [1,2,3,4], "year": 2021, "colors": ["yellow","green"]},
    work_queue_name="default"
)

if __name__ == "__main__":
    main_deployment.apply()