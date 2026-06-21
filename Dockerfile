FROM clickhouse/clickhouse-server:latest

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install clickhouse-driver

RUN mkdir -p /opt/clickhouse/udf

RUN wget https://github.com/Altinity/clickhouse-backup/releases/download/v2.7.2/clickhouse-backup_2.7.2_arm64.deb -O clickhouse-backup_2.7.2_arm64.deb \
    && dpkg -i clickhouse-backup_2.7.2_arm64.deb \
	&& rm clickhouse-backup_2.7.2_arm64.deb \
    && mv /etc/clickhouse-backup/config.yml.example /etc/clickhouse-backup/config.yml
