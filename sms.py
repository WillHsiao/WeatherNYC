import boto3, os, json

def sendsms(pnum, msg):
	with open('../key') as p:
		k = json.load(p)
	client = boto3.client(
		"sns",
		aws_access_key_id = k['aws_access_key_id'],
		aws_secret_access_key = k['aws_secret_access_key'],
		region_name="us-east-1"
	)

	# Send your sms message.
	client.publish(
		PhoneNumber = pnum,
		Message = msg
	)

for filename in os.listdir('sns'):
	if filename[:3] != 'sms':
		continue
	with open('sns/' + filename) as p:
		u = json.load(p)
	sendsms(u['phone'],u['msg'])
	os.remove('sns/' + filename)
