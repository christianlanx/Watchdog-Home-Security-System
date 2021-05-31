'''
Author: Christian Lancaster
Name: BME280 exporter
Function: 
    - Connects to BME280 over i2c. 
    - Retrieves sensor data and publishes to metrics endpoint
'''

# Standard Library Imports
import os
import time
import busio
import logging

# Third-Party Imports
import board
import adafruit_bme280
from flask import Flask, send_file, request, Response
from prometheus_client import start_http_server, Gauge, generate_latest

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create library object using our Bus SPI port
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# Defaults to 1013.25 hPa. Override via service variables.
bme280.sea_level_pressure = os.environ.get('SEA_LEVEL_PRESSURE')

logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

# grab the device name
device_name = os.environ.get('BALENA_DEVICE_NAME_AT_INIT')

# Create a metrics to track sensor data
# Include name, description, and label names
BME280_TEMPERATURE = Gauge(
    'bme280_temperature_celsius', 
    'Temperature sensed by the BME280',
    ['device_name']
)
BME280_TEMPERATURE.labels(device_name)
BME280_RELATIVE_HUMIDITY = Gauge(
    'bme280_relative_humidity',
    'Humidity sensed by the BME280',
    ['device_name']
)
BME280_RELATIVE_HUMIDITY.labels(device_name)
BME280_PRESSURE = Gauge(
    'bme280_pressure_hPa',
    'Pressure sensed by the BME280',
    ['device_name']
)
BME280_PRESSURE.labels(device_name)
BME280_ALTITUDE = Gauge(
    'bme280_altitude_meters',
    'Altitude sensed by the BME280',
    ['device_name']
)
BME280_ALTITUDE.labels(device_name)

@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""
    try:
        BME280_TEMPERATURE.labels(device_name=device_name).set(bme280.temperature)
    except Exception as e:
        logger.error("Failed to update temperature. Exception: {}".format(e))
    try:
        BME280_RELATIVE_HUMIDITY.labels(device_name=device_name).set(bme280.relative_humidity)
    except Exception as e:
        logger.error("Failed to update relative humidity. Exception: {}".format(e))
    try:
        BME280_PRESSURE.labels(device_name=device_name).set(bme280.pressure)
    except Exception as e:
        logger.error("Failed to update pressure. Exception: {}".format(e))
    try:
        BME280_ALTITUDE.labels(device_name=device_name).set(bme280.altitude)
    except Exception as e:
        logger.error("Failed to update altitude. Exception: {}".format(e))

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# OLD FLASK CODE
# app = Flask(__name__)

# @app.route('/')
# def getSensorDataJson():
#     sensorData = {
#         "Temperature": "%0.1f C" % bme280.temperature,
#         "Humidity": "%0.1f C" % bme280.relative_humidity,
#         "Pressure": "%0.1f hPa" % bme280.pressure,
#         "Altitude": "%0.2f meters" %bme280.altitude
#     }
#     return json.dumps(sensorData)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9100)