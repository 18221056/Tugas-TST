## CHANGE THE .ENV CONFIGURATION
```bash
mv .example.env .env
nano .env
```

```bash
DB_NAME="task-manager"
DB_USERNAME="root"
DB_PASSWORD="root"
MODE="PROD" # DEV = DEVELOPMENT / LOCAL | PROD = PRODUCTION / ON SERVER
```

## INSTALL DEPENDENCIES
```bash
pip install -r requirements.txt
```

## RUN ON LOCAL

```bash
uvicorn app:app --reload
```

## RUN ON SERVER

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## RUN ON DOCKER
```bash
sudo docker build -t task-manager:v1 .
sudo docker compose up -d
```