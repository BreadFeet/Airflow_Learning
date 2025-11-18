## Installation on Ubuntu
Airflow installed on Docker Compose
- [1) Docker Installation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
- [2) Docker Desktop Installation](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)
- [3) Airflow Installation in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

## How to Get into the Container System
Get the docker CONTAINER ID of the scheduler.
```
docker ps
```
Open the bash (or other program) in the container system.
```
docker exec -it [CONTAINER ID of the scheduler] bash
```
For example, to see what airflow provider version is installed,
```
pip list | grep airflow
```

## How to Set Up the MinIO Connection in Airflow
### Network Connection
MinIO doesn't require installation or download. Acess ID and password can be set as you wish [[ref](MINIO_run)]. Running the image in docker suffices.
When Airflow is running in Docker Compose while MinIO in Docker, they are not in the same docker network.
```
docker network ls
```
There is a name 'my_project_default' for Airflow project. To connect MinIO to this network,
```
# docker network connect [NETWORK NAME] [CONTAINER NAME]
docker network connect airflow_learning_default minio
```
To check if MinIO gets into the network successfully, either of below can be used.
```
# Check 'Networks' at the end
docker inspect minio  
# Check 'Containers' at the end
docker network inspect airflow_learning_default 
```
### Airflow Connection
Then go to Airflow web UI Connection page. Connection type is 'Amazon Web Services' (not S3 anymore). Don't fill in 'AWS Access Key ID' and 'AWS Secret Acess Key' field but use 'Extra Field JSON' for both.
```
{
  "aws_access_key_id": "miniouser",
  "aws_secret_access_key": "miniopassword",
  "endpoint_url": "http://minio:9000"
}
```
The point is, after the network connection, `endpoint_url` is `http://[CONTAINER_NAME]:9000`.
