from twilio.rest import Client

account_sid = 'xxxx'
auth_token = 'xxxx'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+16077033855',
  body='Hi this is test SMS',
  to='+918699153200'
)

print(message.sid)
