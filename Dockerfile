FROM python:3.10-bullseye

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    unzip libaio1 libssl-dev libffi-dev python3-dev cron tzdata && \
    apt-get clean

# Definir timezone
ENV TZ=America/Asuncion

# Instalar Oracle Instant Client
COPY instantclient-basiclite-linux.x64-21.18.0.0.0dbru.zip /tmp/
RUN unzip /tmp/instantclient-basiclite-linux.x64-21.18.0.0.0dbru.zip -d /opt/oracle && \
    rm /tmp/instantclient-basiclite-linux.x64-21.18.0.0.0dbru.zip && \
    echo /opt/oracle/instantclient_21_18 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_18

# Copiar arquivos da aplicação
COPY . /app
WORKDIR /app

# Instalar dependências Python
RUN pip install --upgrade pip
COPY oracledb-3.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl /tmp/
RUN pip install /tmp/oracledb-3.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl
RUN chmod 0644 /app/crontab.txt
RUN crontab /app/crontab.txt
RUN pip install --no-cache-dir -r requirements.txt

# Iniciar cron
CMD ["cron", "-f"]
