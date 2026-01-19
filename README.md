# Airflow + Spark + PostgreSQL Data Pipeline

This project implements a data pipeline that:  
- Extracts data from a public API  
- Loads raw data into PostgreSQL (staging schema)  
- Processes data using Apache Spark  
- Stores processed data in the `processed` schema  

## Tech Stack
- **Apache Airflow** – Workflow orchestration  
- **PostgreSQL** – Data storage  
- **PySpark** – Data processing  
- **Docker / Docker Compose** – Containerization  

## Architecture Diagram
![Pipeline Diagram](images/schema.png)

## Getting Started
Build and run the pipeline using Docker Compose:

```bash
docker compose up --build
