FROM prom/alertmanager

WORKDIR /alertmanager

COPY ./alertmanager.yml alertmanager.yml

CMD ["--config.file=alertmanager.yml"]