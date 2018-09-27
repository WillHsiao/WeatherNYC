from flask import Flask, render_template, request
import requests

import csv, json
from geojson import Feature, FeatureCollection, Point

def GetForecastURL(url, fname):
	print(fname)
	print(url)
	token = 'kSOuCoucFpFZxAgfjKIYTuwjDBaFCBka'
	creds = dict(token=token)
 
	r1 = requests.get(url, headers=creds)
	urlNew = r1.json()['properties']['forecastGridData']
	urlNew2= r1.json()['properties']['forecast']

	r2 = requests.get(urlNew, headers=creds)
	with open("wdata/" + fname, 'wb') as handle:
		for block in r2.iter_content(1024):
			handle.write(block)

	r2 = requests.get(urlNew2, headers=creds)
	with open("wdata/" + fname + '_f', 'wb') as handle:
		for block in r2.iter_content(1024):
			handle.write(block)

with open('ziplist_geo.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	next(reader, None)
	for A, borough, area, zipCode, helper, latitude, longitude in reader:
		url = 'https://api.weather.gov/points/' + latitude + ',' + longitude
		GetForecastURL(url, zipCode)
