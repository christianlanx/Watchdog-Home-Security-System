FROM prom/alertmanager

WORKDIR /alertmanager

COPY ./alertmanager.yml /alertmanager/alertmanager.yml

CMD ["--config.file=alertmanager.yml"]