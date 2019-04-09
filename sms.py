import boto3, os, json, time

def sendsms(pnum, msg):
	with open('../key') as p:
		k = json.load(p)
	client = boto3.client(
		"sns",
		aws_access_key_id = k['aws_access_key_id'],
		aws_secret_access_key = k['aws_secret_access_key'],
		region_name="us-east-1"
	)

	# set message type
	#response = client.set_sms_attributes(
	#	attributes = {
	#		'DefaultSMSType': 'Transactional'
	#	}
	#)

	# Send your sms message.
	response = client.publish(
		PhoneNumber = pnum,
		Message = msg
	)
	print("Response: {}".format(response))

for filename in os.listdir('sns'):
	if filename[:3] != 'sms':
		continue
	with open('sns/' + filename) as p:
		u = json.load(p)
	sendsms(u['phone'],u['msg'])
	#print(u['phone'],u['msg'])
	time.sleep(3)
	os.remove('sns/' + filename)
