import os
from time import sleep
from twilio.rest import Client
import logging
from flask import Flask, send_file, request, Response
from prometheus_client import start_http_server, Gauge, generate_latest
import json

# get Twilio variables from the environment (Balena device variables)
account_sid = os.environ['TWILIO_ACCOUNT_SID']      # The user's Twilio SID
auth_token = os.environ['TWILIO_AUTH_TOKEN']        # The user's Twilio authentication token
dest_num = os.environ['DEST_NUM']                   # The user's Twilio number used to send alerts
host_num = os.environ['HOST_NUM']                   # The user's phone number that will recieve alerts

latest_message_sid = ""     # used to keep track of the SID of the last message sent

# set up the Twilio client
client = Client(account_sid, auth_token)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

@app.route('/', methods=['POST', 'GET'])
def send_data():
    if request.method == 'POST':
        print("Successful POST request made to Twilio")

        """ ----> Implement the HTTP response stuff from Prometheus here <---- """
        # data = request.form
        data = request.get_json()

        print("POST request success -- New data sent to Twilio")
        # print("The data sent was of type: ", type(data))

        """ Prometheus should send JSON's formatting like this:
        {
            "version": "4",
            "groupKey": <string>,              // key identifying the group of alerts (e.g. to deduplicate)
            "truncatedAlerts": <int>,          // how many alerts have been truncated due to "max_alerts"
            "status": "<resolved|firing>",
            "receiver": <string>,
            "groupLabels": <object>,
            "commonLabels": <object>,
            "commonAnnotations": <object>,
            "externalURL": <string>,           // backlink to the Alertmanager.
            "alerts": [
                {
                    "status": "<resolved|firing>",
                    "labels": <object>,
                    "annotations": <object>,
                    "startsAt": "<rfc3339>",
                    "endsAt": "<rfc3339>",
                    "generatorURL": <string>       // identifies the entity that caused the alert
                }
            ]
        }
        
        see https://prometheus.io/docs/alerting/latest/configuration/#webhook_config
        for more information
        """

        """ implement basic message body using data from "alerts" tag in the JSON object """

        # TODO: create a robust system for creating a message body based on the JSON's sent by Prometheus
        if data.get('alerts'):      # check if 'alerts' tag exists in JSON
            alerts_data = data.get('alerts')[0]
            # print("Found 'alerts' section in JSON -- fetching data")
            # print("The data found was of type:", type(alerts_data))
            # print("Let's try to print it:\n", alerts_data )

        # only send an SMS message if the alert is firing
        if alerts_data['status'] == "firing":

            """ <insert a ton of if-statements here to create the message body> """

            description = alerts_data['annotations']['description']
            summary     = alerts_data['annotations']['summary']

            body = f'\nAlert: {description}\nSummary: {summary}'
        else:
            body = "Error in SMS body creation. See Balena dashboard for more details."

        # send the SMS message
        message = client.messages \
                            .create(
                                 body=body,
                                 from_=host_num,  # used to be `from_='+18135194665'`
                                 to=dest_num      # used to be `to='+13852260092'`
                             )

        # update the latest SID value
        latest_message_sid = str(message.sid)

        # print the message ID
        print("Message sent with ID: ", latest_message_sid)

        return json.dumps(data)


    elif request.method == 'GET':
        string = {

            # Create Influxdb datapoints (using lineprotocol as of Influxdb >1.1) ??
            # See example code from: http://www.igfasouza.com/blog/raspberry-pi-with-influxdb-and-grafana/
            'latest_message_sid': latest_message_sid,
        }
        return json.dumps(string)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5152)