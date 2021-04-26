import time

import board
import busio
import adafruit_bme280

import json

from flask import Flask

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create library object using our Bus SPI port
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25



app = Flask(__name__)

@app.route('/')
def getSensorDataJson():
    sensorData = {

        # Create Influxdb datapoints (using lineprotocol as of Influxdb >1.1) ??
        # See example code from: http://www.igfasouza.com/blog/raspberry-pi-with-influxdb-and-grafana/
        'measurement': 'balena-sense',
        'fields': {
            "Temperature": "%0.1f C" % bme280.temperature,
            "Humidity": "%0.1f C" % bme280.relative_humidity,
            "Pressure": "%0.1f hPa" % bme280.pressure,
            "Altitude": "%0.2f meters" %bme280.altitude
            }
        }
    return json.dumps(sensorData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)