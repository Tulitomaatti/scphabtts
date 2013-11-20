# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for 
from werkzeug import secure_filename
from hiscore import Hiscore

import pickle

import urllib2
from bs4 import BeautifulSoup

MAGIC_URL = "http://www.omatlahdot.fi/omatlahdot/web?command=embedded&action=view&c=15&o=1&s=1220182"

app = Flask(__name__)

@app.route("/bussit")
def fuuboar():
    resp = urllib2.urlopen(MAGIC_URL)
    soup = BeautifulSoup(resp.read())

    timetable = soup.table

    times = timetable.find_all(class_="timecol") # works nicely
    buses = timetable.find_all(class_="linecol")
    dests = timetable.find_all(class_="destcol")
    
    data = []
    for i in xrange(15):
        data.append( [times[i], buses[i], dests[i]] )

    return render_template('schpatts.html', data=data)

@app.route("/newscore", methods=['POST', 'GET'])
def addscore():
    if request.method == 'POST':

        form = request.form

        nick = form['nick']
        game = form['game']
        score = form['score']
        scoretype = form['scoretype']


        new_score = Hiscore(nick, game, score, scoretype)
        # Assuming that hiscores.txt doesn't exist or has a hiscore or an empty list pickled
        scores = []

        try:
            f = open("hiscores.txt", "rb")
            scores = pickle.load(f)
        except Exception:
            f = open("hiscores.txt", "wb")
            pickle.dump(scores, f)

        f.close()

        scores.append(new_score)

        f = open("hiscores.txt", "wb")
        pickle.dump(scores, f)
        f.close()

        return "Score stored! Yay!\n "+ str(new_score)

    else:

    #     return 'lol'
        return render_template('addscore.html')

@app.route("/hiscore")
def hiscore():
    f = open("hiscores.txt", "r")
    scores = pickle.load(f)

    string = ""

    for score in scores:
        string += str(score)

    # Palauta html suoraan: 
    return string

    # Anna templaten hoitaa hommat: 
    # return render_template('template.html', templatenmuuttuja = muuttuja)

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
