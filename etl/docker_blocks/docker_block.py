from prefect.infrastructure.docker import DockerContainer

#alternate to creating Docker Container block in UI
docker_block = DockerContainer(
    image="emczap/prefect:etl_web_to_gcs",
    image_pull_policy="ALWAYS",
    #auto_remove=True,
    network_mode="bridge"
)

docker_block.save('etl-gcs-block', overwrite=True)

