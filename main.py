# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from hiscore import Hiscore

import pickle

import urllib2
from bs4 import BeautifulSoup

MAGIC_URL = "http://www.omatlahdot.fi/omatlahdot/web?command=embedded&action=view&c=15&o=1&s=1220182"
MAGIC_NUMBER = 1
SCORE_SHOW_NUMBER_MAGIC_VARIABLE = 5

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
        # Assuming that hiscores.hax doesn't exist or has a hiscore or an empty list pickled
        scores = []

        try:
            f = open("hiscores.hax", "rb")
            scores = pickle.load(f)
        except Exception:
            f = open("hiscores.hax", "wb")
            pickle.dump(scores, f)

        f.close()

        scores.append(new_score)

        f = open("hiscores.hax", "wb")
        pickle.dump(scores, f)
        f.close()

        return "Score stored! Yay!\n "+ str(new_score)

    else:

    #     return 'lol'
        return render_template('addscore.html')

@app.route("/hiscore")
def hiscore():
    f = open("hiscores.hax", "r")
    scores = pickle.load(f)
    games = []
    template_scores = []
    scores2 = []

    global MAGIC_NUMBER

    for score in scores:
        games.append(score.game)

    # remove duplicates / get 1 of each game
    games = list(set(games))


    template_game = games[MAGIC_NUMBER%len(games)]
    game2 = games[(MAGIC_NUMBER -1 )%len(games)]
    MAGIC_NUMBER += 1

    for score in scores:
        if score.game == template_game:
            template_scores.append(score)
        if score.game == game2:
            scores2.append(score)



    template_scores.sort()
    scores2.sort()

    if template_scores[0].scoretype == "points":
        template_scores.reverse()

    if scores2[0].scoretype == "points":
        scores2.reverse()


    template_scores = template_scores[:SCORE_SHOW_NUMBER_MAGIC_VARIABLE]
    scores2 = scores2[:SCORE_SHOW_NUMBER_MAGIC_VARIABLE]


    # Palauta html suoraan: 
    # return string

    # Anna templaten hoitaa hommat: 
    return render_template('hiscore.html', game = template_game, scores = template_scores, game2 = game2, scores2 = scores2)

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
