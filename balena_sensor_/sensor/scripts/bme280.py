import subprocess
import json
import threading
import io
import time

# import the bme280 needed libraries!
import board
import busio
import adafruit_bme280

class BME280:
    data = None

    def __init__(self, readfrom):
        self.i2c = busio.I2C(board.SCL, board.SDA)   # establish I2C library (??)
        if readfrom == 'bme280secondary':
            # self.command = ['/usr/src/app/bsec_bme680_linux/bsec_bme680', 'secondary']
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, address = 0x76)
        else:
            # self.command = ['/usr/src/app/bsec_bme680_linux/bsec_bme680']
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)

        # self.capture_thread = threading.Thread(target=self.capturewrap)
        # self.capture_thread.start()

    # def capturewrap(self):
    #     while True:
    #         try:
    #             self.capture()
    #         except BaseException as e:
    #             print('{!r}; restarting capture thread'.format(e))
    #         else:
    #             print('Capture thread exited; restarting')
    #         time.sleep(5)

    # def capture(self):
    #     # Start the process and commence capture and parsing of the output
    #     process = subprocess.Popen(self.command, stdout=subprocess.PIPE)
    #
    #     for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
    #         self.data = json.loads(line.strip())
    #
    #     rc = process.poll()
    #     time.sleep(2)
    #     return rc

    def get_readings(self, sensor):
        return [
            {
                'measurement': 'balena-sense',
                'fields': {
                    'temperature': float(self.bme280.temperature),
                    'pressure': float(self.bme280.pressure),
                    'humidity': float(self.bme280.relative_humidity),
                    'air_quality_score': None,
                    'air_quality_score_accuracy': None,
                    'eco2_ppm': None,
                    'bvoce_ppm': None
                }
            }
        ]
