# yup_trash_day

i keep missing trash day - i wanted to fix that.

## Description
flask app ran locally to notify the user via sms/mms that it is either trash or recycle day.

## Usage
`.env` 

information here is referenced by the app, see [twilio documentation](https://www.twilio.com/docs/sms/quickstart/python) on how to set up twilio account
```bash
TWILIO_ACCOUNT_SID=''
TWILIO_AUTH_TOKEN=''
TWILIO_PHONE_NUMBER=''
RECEIVER_PHONE_NUMBER=''
MESSAGING_SERVICE_SID=''
```

`install requirements`
```python
pip install -r requirements.txt
```
`configure app & run`
```bash
export FLASK_APP=app.py
flask run
```
`configure ngrok & run`

the [ngrok docs](https://dashboard.ngrok.com/get-started/setup) are great.
also [this](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html)
```bash
ngrok config add-authtoken <token>
ngrok http 5000
```
`twilio webhook`

set the generated ngrok forwarding url as the twilio's phone numbers recieving message webhook in UI

`cron sms_webhook.py`

## Future
- [ ] Dockerize
- [ ] Enhance reminder feature

