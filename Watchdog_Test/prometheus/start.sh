#!/bin/bash
# Start Prometheus with the updated config file
chmod a+x ./prometheus/prometheus
./prometheus/prometheus --config.file=/etc/prometheus/prometheus.yml
#./prometheus/alertmanager --config.file=alertmanager.yml