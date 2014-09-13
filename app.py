#!/usr/bin/python

from flask import Flask, render_template, url_for, flash, request, session
import geoip2.database

app = Flask(__name__)
app.secret_key = '42'

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('layout.html')

@app.route('/loadData', methods = ['GET', 'POST'])
def loadData():
    if request.method == 'POST':
        ips = request.form['ipAddressBox'].split()
        geoipAttributes = dict()
        for ip in ips:
            geoipAttributes[ip] = getGeoipAttributes(ip)
        return render_template('viewMap.html', geoipAttributes=geoipAttributes)
    if request.method == 'GET':
        return render_template('loadData.html')

@app.route('/viewMap', methods = ['GET', 'POST'])
def viewMap(geoipAttributes = None):
    return render_template('viewMap.html', geoipAttributes=geoipAttributes)

readerCity = geoip2.database.Reader('GeoIP2-City.mmdb')
readerISP = geoip2.database.Reader('GeoIP2-ISP.mmdb')

def getGeoipAttributes(ip):
    responseCity = readerCity.city(ip)
    responseISP = readerISP.omni(ip)
    return {'lat':responseCity.location.latitude, 'long':responseCity.location.longitude, 'city':responseCity.city.name, 'postCode':responseCity.postal.code, 'org':responseISP.raw['organization'], 'isp':responseISP.raw['isp']}

if __name__ == "__main__":
    app.run(debug=True, port=5000)

