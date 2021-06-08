# EE 475 Embedded Systems Capstone
# Team 5
### Christian Lancaster, Jamie Thorup, Joseph Chao, Morgan McCandless, Rouen de la O

## Watchdog Home Security System
Watchdog is an IoT monitoring device that monitors multiple sensors and alerts the user to anomalous conditions.

### Getting started

* Raspberry Pi 4
* BME280 sensor [example](https://es.aliexpress.com/item/1005001621866431.html)
* Sparkfun noise sensor
* STM 32 Discovery board
* Raspberry Pi Camera

* A balenaCloud account ([sign up here](https://dashboard.balena-cloud.com/))
* [balenaEtcher](https://balena.io/etcher)

Once all of this is ready, you are able to deploy this repository following instructions below.

### Connect the hardware

To connect the BME280 with the Raspberry Pi follow this diagram connections below:

![alt text](https://github.com/balena-io-playground/python-bme280/blob/main/bme280-raspberrypi4.png)

To connect the Sensor hub with the Raspberry Pi, follow the below diagram

### Deploy the code

#### Deploy with balena

Running this project is as simple as deploying it to a balenaCloud application. You can do it in just one click by using the button below:

[![](https://www.balena.io/deploy.png)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/christianlanx/EE475)

Follow instructions, click Add a Device and flash an SD card with that OS image dowloaded from balenaCloud. Enjoy the magic 🌟Over-The-Air🌟!

#### balena CLI

If you are a balena CLI expert, feel free to use balena CLI.

- Sign up on [balena.io](https://dashboard.balena.io/signup)
- Create a new application on balenaCloud.
- Clone this repository to your local workspace.
- Using [Balena CLI](https://www.balena.io/docs/reference/cli/), push the code with `balena push <application-name>`
- See the magic happening, your device is getting updated 🌟Over-The-Air🌟!