#!/usr/bin/env python

from flask import Flask, render_template, url_for, flash, request, session
import geoip2.database

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
            try:
                geoipAttributes[ip] = getGeoipAttributes(ip)
            except:
                flash('An error occurred processing IP ' + ip)
        session['geoipAttributes'] = geoipAttributes
        flash('Geolocated ' + str(len(geoipAttributes)) + ' IP addresses.')
    return render_template('loadData.html')

@app.route('/viewMap', methods = ['GET', 'POST'])
def viewMap():
    geoipAttributes = session['geoipAttributes']
    return render_template('viewMap.html', geoipAttributes=geoipAttributes)

@app.route('/viewTable', methods = ['GET', 'POST'])
def viewTable():
    geoipAttributes = session['geoipAttributes']
    return render_template('viewTable.html', geoipAttributes=geoipAttributes)

readerCity = geoip2.database.Reader('GeoIP2-City.mmdb')
readerISP = geoip2.database.Reader('GeoIP2-ISP.mmdb')

def getGeoipAttributes(ip):
    responseCity = readerCity.city(ip)
    responseISP = readerISP.isp(ip)
    return {'lat':responseCity.raw[u'location'][u'latitude'], 'long':responseCity.raw[u'location'][u'longitude'], \
            'city':responseCity.raw[u'city'][u'names'][u'en'], 'postcode':responseCity.raw[u'postal'][u'code'], \
            'subdivision':responseCity.raw[u'subdivisions'][0][u'names'][u'en'], \
            'country':responseCity.raw[u'country'][u'names'][u'en'], 'org':readerISP.isp(ip).__dict__['organization'], \
            'isp':readerISP.isp(ip).__dict__['isp']}

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

