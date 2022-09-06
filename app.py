from flask import Flask, request, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# load env variables
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECEIVER_PHONE_NUMBER = os.getenv('RECEIVER_PHONE_NUMBER')
MESSAGING_SERVICE_SID = os.getenv('MESSAGING_SERVICE_SID')

#global variables
dt = datetime.now()
day = dt.weekday()
if day == 1 or day == 4:
    bin_type = "trash"
elif day == 2:
    bin_type = "recycling"
else:
    bin_type = "testing"

# account information
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
app = Flask(__name__)

# A route that tests app health
@app.route('/')
def health():
    return "This app is running!"

# A route that sends a SMS message
@app.route('/sms')
def send_sms():
    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            to=RECEIVER_PHONE_NUMBER,
            body=f"Today is {bin_type} day! Did you take out the bins??",
            media_url=['https://media.giphy.com/media/fUjNpJtQDfl28CCFoF/giphy.gif'],
        )
        if message.sid:
            message = 'message successfully sent'
        else:
            message = 'message was not successfully sent'
        return message
    except UnboundLocalError as err:
        return 'There is nothing to do today'

@app.route('/reminder', methods=['POST'])
def reminder():
    send_when = datetime.utcnow() + timedelta(minutes=16)
    message = client.messages.create(
        messaging_service_sid=MESSAGING_SERVICE_SID,
        from_=TWILIO_PHONE_NUMBER,
        to=RECEIVER_PHONE_NUMBER,
        body=f"{bin_type.upper()} day! Did you take out the bins??",
        schedule_type='fixed',
        send_at=send_when.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    if message.sid:
        message = 'reminder successfully sent'
    else:
        message = 'reminder did not send'
    
    return message

# trigger a reply when /sms hit 
# A route to respond to SMS messages
@app.route('/sms_reply', methods=['GET', 'POST'])
def incoming_sms():
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    if body == 'y':
        resp.message("Good Job Boi")
    elif body == 'n':
        msg = resp.message(f"Dude, TAKE THE BINS OUT!?!?")
        return redirect(url_for('reminder'))
    else:
        resp.message("Only 'y' or 'n'")

    return str(resp)

if __name__ == '__main__':
   app.run(debug=True)