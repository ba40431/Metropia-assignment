# Metropia-assignment

## How to deploy the service

- Build Docker Image.

```
docker build -t ba40431/travel-project:2022-08-05 .
```

- PUSH Docker Image To Docker Hub

```
docker push ba40431/travel-project:2022-08-05
```

- PULL Docker Image To EC2

```
sudo docker pull ba40431/travel-project:2022-08-05
```

- Run Docker Image

```
sudo docker compose up
```

## How to perform the unit test


## How to perform the DB migration process

Use the RDS MySQL database directly.

## Swagger document URL

URL : http://54.221.150.42/swagger