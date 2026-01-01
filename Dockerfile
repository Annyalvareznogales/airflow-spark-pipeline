# Dockerfile personalizado para Airflow + uv
FROM apache/airflow:3.1.5-python3.12

USER root

# Instalar compiladores, librerías de Postgres, Java y utilidades de Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    openjdk-17-jdk \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar JAVA_HOME y PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH


# Actualizar pip y setuptools
RUN python -m pip install --upgrade pip setuptools wheel

# Copiar requirements.txt
COPY requirements.txt /opt/airflow/requirements.txt

RUN python -m pip install --no-cache-dir uv
RUN uv pip install --system -r /opt/airflow/requirements.txt

RUN chown -R airflow:root /opt/airflow

USER ${AIRFLOW_UID:-50000}:0

# Variables de entorno
ENV AIRFLOW_HOME=/opt/airflow

# Entrypoint y comando por defecto de Airflow
ENTRYPOINT ["/entrypoint"]
CMD ["webserver"]