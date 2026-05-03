FROM clickhouse/clickhouse-server:latest

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install clickhouse-driver

