'''
Author: Jamie Thorup
Name: Twilio SMS
Function:
    - Parses JSON data sent via POST requests from the Prometheus container
    - Creates an SMS message body from the data retrieved from JSON object
    - Uses Twilio to send an SMS message to the user's phone when an alert is to be broadcast
'''

# import packages
import os
from time import sleep
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import logging
from flask import Flask, send_file, request, Response
from prometheus_client import start_http_server, Gauge, generate_latest
import json

# get Twilio variables from the environment (Balena device variables)
account_sid = os.environ['TWILIO_ACCOUNT_SID']      # The user's Twilio SID
auth_token = os.environ['TWILIO_AUTH_TOKEN']        # The user's Twilio authentication token
dest_num = os.environ['DEST_NUM']                   # The user's Twilio number used to send alerts
host_num = os.environ['HOST_NUM']                   # The user's phone number that will receive alerts

latest_message_sid = ""     # used to keep track of the SID of the last message sent

# set up the Twilio client
client = Client(account_sid, auth_token)

logger = logging.getLogger(__name__)
app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

@app.route('/', methods=['POST', 'GET'])
def send_data():
    if request.method == 'POST':

        user_resp = request.values.get('Body', None)    # get the text from the user's SMS response
        if user_resp is None:
            data = request.get_json()   # get the alert JSON data from the POST request
        else:
            # Start our TwiML response
            resp = MessagingResponse()
            return str(resp)

        print("POST request success -- New data sent to Twilio")
        # print("new data:\n", user_resp)

        """ Prometheus should send JSON's formatted like this:
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
        
        for more information, see:
        https://prometheus.io/docs/alerting/latest/configuration/#webhook_config
        """

        """ implement basic message body using data from "alerts" tag in the JSON object """

        # TODO: create a robust system for creating a message body based on the JSON's sent by Prometheus
        if data.get('alerts'):      # check if 'alerts' tag exists in JSON
            alerts_data = data.get('alerts')[0]

        # only send an SMS message if the alert is firing
        if alerts_data['status'] == "firing":

            # parse the JSON object for info to put in SMS body
            description = alerts_data['annotations']['description']
            summary     = alerts_data['annotations']['summary']

            # create the SMS messages' body
            body = f'\nAlert: {description}\nSummary: {summary}'
        else:
            body = "Error in SMS body creation. See Balena dashboard for more details."

        # send the SMS message
        message = client.messages \
                            .create(
                                 body=body,
                                 from_=host_num,
                                 to=dest_num
                             )

        # update the latest SID value
        latest_message_sid = str(message.sid)

        # print the message ID
        print("Message sent to phone with ID: ", latest_message_sid)

        return json.dumps(data)


    # Provide access to information in the Twilio alert container -- CURRENTLY UNSUPPORTED
    elif request.method == 'GET':
        string = {
            'latest_message_sid': latest_message_sid,
        }
        return json.dumps(string)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5152)