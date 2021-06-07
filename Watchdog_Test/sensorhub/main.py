"""
Authors: Rouen de la O && Christian Lancaster
Title: Sensorhub main
Purpose: Retrieves data from the sensor hub via uart, publishes that data to prometheus
"""

# Standard Library Imports
import os
import logging
import serial
# Third-Party Imports
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest

# Read data from UART, formatted a certain way :)
serial_data = lambda : int(str(serial.Serial("/dev/serial0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=5).read(3))[2:-1])

logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

device_name = os.environ.get('BALENA_DEVICE_NAME_AT_INIT')

SENSORHUB_NOISELEVEL = Gauge(
    'sensorhub_noiselevel',
    'SensorHub relative noise level',
    ['device_name']
)
SENSORHUB_NOISELEVEL.labels(device_name)

@app.route('/metrics', methods=['GET'])
def get_reading():
    try:
        SENSORHUB_NOISELEVEL.labels(device_name=device_name).set(serial_data())
    except Exception as e:
        logger.error("Failed to update noise level. Exception: {}".format(e))
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)