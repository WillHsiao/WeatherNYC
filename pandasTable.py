from flask import Flask,render_template, request
import requests
import pandas as pd
import numpy as np
import json
app = Flask(__name__)
 
@app.route("/")
def index():
 
#	r = requests.get(url, headers=creds)
	with open('wdata/10004') as f:
		r = json.load(f)

	df1 = pd.DataFrame(r['properties']['temperature']['values'])
	df1.columns = ['Time', 'Temperature']
	df1['Time']=df1['Time'].str[:19]

	df2 = pd.DataFrame(r['properties']['windSpeed']['values'])
	df2.columns = ['Time', 'Wind Speed']
	df2['Time']=df2['Time'].str[:19]

	df = pd.merge(df1, df2, how='outer', on=['Time'])
	df = df.sort_values(by='Time')
	df = df.fillna('')
	desc = df1.describe(include='all')
	return render_template("d.html", data=df.to_html(), stat=desc.to_html())

if __name__ == "__main__":
	app.run(host='0.0.0.0')

