from twilio.rest import Client

account_sid = 'AC2dc43b8f258494314aa2330f1c9cb259'
auth_token = '755a842c82734f024ff8443b84ba10f4'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+16077033855',
  body='Hi this is test SMS',
  to='+918699153200'
)

print(message.sid)