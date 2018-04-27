#requires gmplot
#install using pip install gmplot
#this code generates my_map.html
#run my_map.html to get the actual map
from gmplot import gmplot
import sqlite3
from math import sin, cos, sqrt, atan2, radians
import sys

if len(sys.argv) < 3:
	print ("Usage : python mapplot.py Cityname Threshold")
	exit()
source = sys.argv[1]
thresh = float(sys.argv[2])
print (source,thresh)

def distance(lat1,lon1,lat2,lon2):
	R = 6373.0
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	dist = R * c
	return dist
def plot(lats,lons,city):
	lat_c = sum(lats)/float(len(lats))
	lon_c = sum(lons)/float(len(lons))
	gmap = gmplot.GoogleMapPlotter(lat_c , lon_c ,8)
	#gmap.scatter(lats,lons, '#FF0000', size=400, marker=True,title="Hii")
	for i in range(len(lats)):
		gmap.marker(lats[i],lons[i],title=city[i])
	gmap.draw("my_map.html")
	
db = "cities.sqlite"
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("SELECT latitude,longitude FROM Cities where city = '"+source+"' ")
rows = cur.fetchone()
#rows = [lambda x : None not in x ,rows]
print(rows)
if len(rows) == 0:
	print ("City Not Found")
	exit()
lat_main = rows[0]
lon_main = rows[1]	
#plot([lat_main],[lon_main])
cur.execute("SELECT city,latitude,longitude FROM Cities WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
rows = cur.fetchall()
print(rows)
#rows = filter(lambda x : None not in x , rows)
#print(len(rows))
rows = map(lambda x : (x[0],x[1],x[2],distance(x[1],x[2],lat_main,lon_main)) , rows)
#print(len(rows))
rows = filter(lambda x : x[3] < thresh , rows)
#print(len(rows))
city, lats, lons = [], [], []
for i in rows :
        city.append(i[0])
        lats.append(i[1])
        lons.append(i[2])
	
#city,lats,lons = [x[0] for x in rows],[x[1] for x in rows],[x[2] for x in rows]
print (lats,lons,city)
plot(lats,lons,city)
