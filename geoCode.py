import geopy
import pandas
from geopy.geocoders import Nominatim, GoogleV3
# versions used: geopy 1.10.0, pandas 0.16.2, python 2.7.8

def main():
  io = pandas.read_csv('ziplist.csv', index_col=None, header=0, sep=",")

  def get_latitude(x):
    return x.latitude

  def get_longitude(x):
    return x.longitude

  #geolocator = Nominatim(timeout=1)
  geolocator = GoogleV3(api_key='')
  # uncomment the geolocator you want to use

  io['helper'] = io['zip'].map(str) + " NY, New York"
  geolocate_column = io['helper'].apply(geolocator.geocode)
  io['latitude'] = geolocate_column.apply(get_latitude)
  io['longitude'] = geolocate_column.apply(get_longitude)
  io.to_csv('ziplist_geo.csv')

if __name__ == '__main__':
  main()
