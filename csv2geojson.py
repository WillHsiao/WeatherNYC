import csv, json, os
import pandas as pd
import numpy as np
from geojson import Feature, FeatureCollection, Point, Polygon
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
	TimeStart = now.astimezone(pytz.timezone("US/Eastern"))
	TimeEnd   = now.astimezone(pytz.timezone("US/Eastern"))
	def __init__(self, r, target, r2):
		self.__r = r
		self.__target = target
		self.__r2 = r2
	def getAll(self):
		df2 = pd.DataFrame(r2['properties']['periods'])
		df2['startTime'] = pd.to_datetime(df2['startTime'].str[:16].replace('T', ' '))
		df2['startTime'] = df2['startTime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
		df2['endTime'] = pd.to_datetime(df2['endTime'].str[:16].replace('T', ' '))
		df2['endTime'] = df2['endTime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

		df = pd.DataFrame(r['properties'][self.__target]['values'])
		df.columns = ['Time', 'c1'] #rename pandas column header
		df['Time'] = pd.to_datetime(df['Time'].str[:16].replace('T', ' ')) #convert to time format
		df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern') #convert to EST time zone

		GetValue.TimeStart = df['Time'].min()
		if GetValue.TimeStart > df['Time'].min():
			GetValue.TimeStart = df['Time'].min()
		if GetValue.TimeEnd   < df['Time'].max():
			GetValue.TimeEnd = df['Time'].max()

		df['TimeStr'] = df['Time'].dt.strftime('%m-%d %H:%M')

		minV = df.loc[df['c1'].idxmin()]
		maxV = df.loc[df['c1'].idxmax()]

		HighTimeRec = df2[(df2['startTime'] <= maxV['Time']) & (df2['endTime'] >= maxV['Time'])]
		LTout = ''
		HTout = ''
		if HighTimeRec.empty == False:
			HTout = str(HighTimeRec['detailedForecast'].iloc[0])
		LowTimeRec  = df2[(df2['startTime'] <= minV['Time']) & (df2['endTime'] >= minV['Time'])]
		if LowTimeRec.empty == False:
			LTout = str(LowTimeRec['detailedForecast'].iloc[0])
		return {'Low':     minV['c1'] ,
			'High':    maxV['c1'] ,
			'LowTime':     str(minV['TimeStr']).replace('T', ' ') ,
			'LowTimeDesc': LTout,
			'HighTime':    str(maxV['TimeStr']).replace('T', ' ') ,
			'HighTimeDesc':HTout
			}

features = []
for filename in os.listdir('wdata'):
	if filename[-1] == 'f':
		continue
	with open('wdata/' + filename + '_f') as f2:
		r2 = json.load(f2)
	with open('wdata/' + filename) as f:
		r = json.load(f)

	df1 = pd.DataFrame(r['properties']['temperature']['values'])
	df1.columns = ['Time', 'Temperature']
	df1['Time'] = df1['Time'].str[:19].replace('T', ' ')
	maxTemp = df1.loc[df1['Temperature'].idxmax()]
	minTemp = df1.loc[df1['Temperature'].idxmin()]

	zInfo = getZipInfo(filename)

	v_temp = GetValue(r, 'temperature', r2)
	v_wind = GetValue(r, 'windSpeed', r2)
	v_snow = GetValue(r, 'snowfallAmount', r2)
	v_rain = GetValue(r, 'quantitativePrecipitation', r2)

	latitude, longitude = map(float, (zInfo['latitude'], zInfo['longitude']))
	features.append(
		Feature(
			geometry = Point((longitude, latitude)),
			properties = {
				'Area': zInfo['area'].to_string(index=False) + ' (' + zInfo['borough'].to_string(index=False) + ')',
				'TempLow':  str(int(round(v_temp.getAll()['Low'] * 1.8 + 32, 0))),
				'TempLowV': int(round(v_temp.getAll()['Low'] * 1.8 + 32, 0)),
				'TempLowTime': v_temp.getAll()['LowTime'],
				'TempLowTimeDesc': v_temp.getAll()['LowTimeDesc'],
				'TempHigh': str(int(round(v_temp.getAll()['High']* 1.8 + 32, 0))),
				'TempHighV': int(round(v_temp.getAll()['High']* 1.8 + 32, 0)),
				'TempHighTime': v_temp.getAll()['HighTime'],
				'TempHighTimeDesc': v_temp.getAll()['HighTimeDesc'],
				'WindHigh': str(round(v_wind.getAll()['High'],1)) + ' mph',
				'WindHighV': round(v_wind.getAll()['High'],1),
				'WindHighTime': v_wind.getAll()['HighTime'],
				'WindHighTimeDesc': v_wind.getAll()['HighTimeDesc'],
				'SnowHigh': str(round(v_snow.getAll()['High'] * 0.0393701,1)) + ' in',
				'SnowHighV': round(v_snow.getAll()['High'] * 0.0393701,1),
				'SnowHighTime': v_snow.getAll()['HighTime'],
				'SnowHighTimeDesc': v_snow.getAll()['HighTimeDesc'],
				'RainHigh': str(round(v_rain.getAll()['High'] * 0.0393701,1)) + ' in',
				'RainHighV': round(v_rain.getAll()['High'] * 0.0393701,1),
				'RainHighTime': v_rain.getAll()['HighTime'],
				'RainHighTimeDesc': v_rain.getAll()['HighTimeDesc']

			}
		)
	)
collection = FeatureCollection(features)

#print(GetValue.TimeStart)
#print(GetValue.TimeEnd)
#GetValue.TimeStart = df['Time'].min().strftime('%m-%d %H:%M')

with open("geojson.json", "w") as f:
	f.write('%s' % collection)
with open("range.txt", "w") as f:
	f.write('%s' % GetValue.TimeStart.strftime('%m-%d %H:%M') + ' to ' + GetValue.TimeEnd.strftime('%m-%d %H:%M'))
