# Metropia-assignment

## How to deploy the service

1. Build Docker Image.

```
docker build -t ba40431/travel-project:2022-08-05 .
```

2. PUSH Docker Image TO Docker Hub

```
docker push ba40431/travel-project:2022-08-05
```

3. PULL Docker Image TO EC2

```
sudo docker pull ba40431/travel-project:2022-08-05
```

4. Run Docker Image

```
sudo docker compose up
```

## How to perform the unit test


## How to perform the DB migration process

Use the RDS MySQL database directly.

## Swagger document URL

URL : http://54.221.150.42/swagger