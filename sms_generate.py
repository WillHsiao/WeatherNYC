import csv, json, os
import pandas as pd
import numpy as np
import json
import pytz
from datetime import datetime

def getZipInfo(zip):
	df = pd.read_csv('ziplist_geo.csv')
	row = df.loc[df['zip'] == int(zip)]
	return row

class GetValue:
	now = pytz.utc.localize(datetime.utcnow())
	TimeNow = now.astimezone(pytz.timezone("US/Eastern"))
	TimeStart = now.astimezone(pytz.timezone("US/Eastern"))
	TimeEnd   = now.astimezone(pytz.timezone("US/Eastern"))
	def __init__(self, r, target):
		self.__r = r
		self.__target = target
	def getAll(self):
		df = pd.DataFrame(r['properties'][self.__target]['values'])
		df.columns = ['Time', 'c1'] #rename pandas column header
		df['Time'] = pd.to_datetime(df['Time'].str[:16].replace('T', ' ')) #convert to time format
		df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern') #convert to EST time zone

		df = df[df['Time'] >= GetValue.TimeNow] #filter out the forecast time in the past
		if df.empty == True:
			return None

		GetValue.TimeStart = df['Time'].min()
		if GetValue.TimeStart > df['Time'].min():
			GetValue.TimeStart = df['Time'].min()
		if GetValue.TimeEnd   < df['Time'].max():
			GetValue.TimeEnd = df['Time'].max()

		df['TimeStr'] = df['Time'].dt.strftime('%m-%d %H:%M')

		minV = df.loc[df['c1'].idxmin()]
		maxV = df.loc[df['c1'].idxmax()]

		return {'Low':     minV['c1'] ,
			'High':    maxV['c1'] ,
			'LowTime':     str(minV['TimeStr']).replace('T', ' ') ,
			'HighTime':    str(maxV['TimeStr']).replace('T', ' ') ,
			}

for filename in os.listdir('sns'):
	with open('sns/' + filename) as p:
		if filename[:3] == 'sms':
			continue
		res = {'templow':0, 'temphigh':0, 'heathigh':0, 'rainhigh':0, 'snowhigh':0, 'windhigh':0}
		resD = {'templow':'temperature lower', 'temphigh':'temperature lower', 'heathigh':'heat higher', 'rainhigh':'rainfall higher', 'snowhigh':'snow accumulation higher', 'windhigh':'wind speed higher'}
		resP = {'templow':'LT', 'temphigh':'HT', 'heathigh':'HH', 'rainhigh':'HR', 'snowhigh':'HS', 'windhigh':'HW'}
		u = json.load(p)
		print(filename + ': ' + u['phone'])
		for filename in os.listdir('wdata'):
			if filename[-1] == 'f' or filename[0] == 'a':
				continue
			with open('wdata/' + filename) as f:
				r = json.load(f)
			zInfo = getZipInfo(filename)

			v_temp = GetValue(r, 'temperature')
			v_wind = GetValue(r, 'windSpeed')
			v_snow = GetValue(r, 'snowfallAmount')
			v_rain = GetValue(r, 'quantitativePrecipitation')
			v_heat = GetValue(r, 'heatIndex')

			if v_temp.getAll() is not None:
				if v_temp.getAll()['Low']*1.8+32 <= float(u['threshold']['templow']):
					res['templow'] += 1
				if v_temp.getAll()['High']*1.8+32 >= float(u['threshold']['temphigh']):
					res['temphigh'] += 1
			if v_heat.getAll() is not None:
				if v_heat.getAll()['High']*1.8+32 >= float(u['threshold']['heathigh']):
					res['heathigh'] += 1
			if v_snow.getAll() is not None:
				if round(v_snow.getAll()['High']*0.0393701,1) >= float(u['threshold']['snowhigh']):
					res['snowhigh'] += 1
			if v_wind.getAll() is not None:
				if v_wind.getAll()['High'] >= float(u['threshold']['windhigh']):
					res['windhigh'] += 1
			if v_rain.getAll() is not None:
				if round(v_rain.getAll()['High']*0.0393701,1) >= float(u['threshold']['rainhigh']):
					res['rainhigh'] += 1
			#latitude, longitude = map(float, (zInfo['latitude'], zInfo['longitude']))
			
	#print(res)
	Msg = ''
	Par = ''
	for x in res:
		if res[x] > 0:
			Par = Par + str(resP[x]) + '=' + str(u['threshold'][x]) + '&'
			Msg = 'NYC Weather Alert: ' + str(res[x]) + ' area(s) have ' + resD[x] + ' than ' + str(u['threshold'][x]) + ' in a week, please visit http://18.222.210.44/?' + Par + ' for detail'
			q = {'phone':'','msg':'','username':''}
			q['phone'] = u['phone']
			q['username'] = u['username']
			q['msg'] = Msg
			q = json.dumps(q)
			print(q)
			with open('sns/sms_' + u['fname'], "w") as f:
				f.write('%s' % q)

#with open("range.txt", "w") as f:
#	f.write('%s' % GetValue.TimeStart.strftime('%m-%d %H:%M') + ' to ' + GetValue.TimeEnd.strftime('%m-%d %H:%M'))
