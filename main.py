# -*- coding: utf-8 -*-
from flask import Flask
from flask import url_for
from flask import render_template

import urllib2
from bs4 import BeautifulSoup

MAGIC_URL = "http://www.omatlahdot.fi/omatlahdot/web?command=embedded&action=view&c=15&o=1&s=1220182"

app = Flask(__name__)

# @app.route("/styles/<name>")
# def asdf(name=None):
#     style = open("static/embedded.css?2","r")
#     return style.read()



@app.route("/aika2")
def getHSL2():
    resp = urllib2.urlopen(MAGIC_URL)
    soup = BeautifulSoup(resp.read())

# Got all times           magic      magic          v-- this is the column number. 
#...     print t.contents[0].contents[3+i].contents[0].string
    timetable = soup.table


    times = timetable.find_all(class_="timecol") # works nicely
    buses = timetable.find_all(class_="linecol")
    dests = timetable.find_all(class_="destcol")
    
    data = []
    for i in xrange(15):
        data.append( [times[i], buses[i], dests[i]] )

    soup.link

    #return soup.prettify()
    return render_template('schpatts.html', data=data)

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
