import csv, json, os
from datetime import datetime

def getZipInfo(zip):
	df = pd.read_csv('ziplist_geo.csv')
	row = df.loc[df['zip'] == int(zip)]
	return row

with open('wdata/alerts') as alertfile:
	a = json.load(alertfile)
	for x in a['features']:
		Msg = x['properties']['headline']
		for filename in os.listdir('sns'):
			with open('sns/' + filename) as p:
				if filename[:3] == 'sms':
					continue
				u = json.load(p)
				print(filename + ' (alert): ' + u['phone'])
			if u['fname'] != 'will': #beta for will only
				continue
			Msg = 'NYC Weather Alert: [' + Msg + '] please visit http://18.222.210.44/ for detail'
			q = {'phone':'','msg':'','username':''}
			q['phone'] = u['phone']
			q['username'] = u['username']
			q['msg'] = Msg
			q = json.dumps(q)
			print(q)
			with open('sns/sms_alert_' + u['fname'] + x['properties']['id'], "w") as f:
				f.write('%s' % q)
