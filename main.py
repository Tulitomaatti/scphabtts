# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from hiscore import Hiscore

import pickle

import urllib2
from bs4 import BeautifulSoup

import os


MAGIC_URL = "http://www.omatlahdot.fi/omatlahdot/web?command=embedded&action=view&c=15&o=1&s=1220182"
MAGIC_NUMBER = 1
SCORE_SHOW_NUMBER_MAGIC_VARIABLE = 8

HISCORES_FILE = os.getenv("HOME") + "/scphabtts/hiscores.hax"

app = Flask(__name__)

@app.route("/")
def adsf():
    return "Go to /hiscore or /newscore or /bussit"

@app.route("/np", methods=['POST', 'GET'])
def fdsa():
    return render_template("nowplaying.html")

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

        try:
            nick = form['nick']
        except KeyError:
            nick = form['newnick']

        try: 
            game = form['game']
        except KeyError:
            game = form['newgame']
            if form['newscoretype'] == "":
                return "Täytä scoretype"

        score = form['score']


        # Assuming that hiscores.hax doesn't exist or has a hiscore or an empty list pickled
        scores = []

        try:
            f = open(HISCORES_FILE, "rb")
            scores = pickle.load(f)
        except IOError:
            try:
                f = open("hiscores.hax.backup", "rb")
                scores = pickle.load(f)
            except IOError:         
                f = open(HISCORES_FILE, "wb")
                pickle.dump(scores, f)

        if form['newgame'] == "":
            game = form['game']
            # also set scoretype: 
            for score_item in scores:
                if score_item.game == game:
                    scoretype = score_item.scoretype
                    break

        else: 
            game = form['newgame']
            scoretype = form['newscoretype']
            #check if game already exists:

            for score_item in scores:
                if score_item.game == game:
                    scoretype = score_item.scoretype
                    break

            if scoretype == '':
                return "Saatanan saatana täytetään se scoretyyppi"


        if form['newnick'] == "":
            nick = form['nick']
        else: 
            nick = form['newnick']

        f.close()


       #debug: return nick + game + score  + scoretype

        new_score = Hiscore(nick, game, score, scoretype)


        scores.append(new_score)

        f = open(HISCORES_FILE, "wb")
        pickle.dump(scores, f)
        f.close()

       # debugstring = str((nick, game, score, scoretype, droptype))
	PASKAHEADI='<meta http-equiv="refresh" content="6; url=/newscore" />'
	PASKAHAKKI="<audio autoplay><source src='https://archive.org/download/GameOverYeah/GameOverYeah.ogg'></audio>"
	
        return PASKAHEADI+"Score stored! Yay!\n "+ str(new_score) + "\n"+PASKAHAKKI#+ debugstring 

    else:
        scoretypes = []
        nicks = []
        games = []

        try: 
            f = open(HISCORES_FILE, "r")
        except IOError:
            return render_template('addscore.html', scoretypes = scoretypes)

        scores = pickle.load(f)

        for score in scores:
            scoretypes.append(score.scoretype)
            nicks.append(score.nick)
            games.append(score.game)

        scoretypes = list(set(scoretypes))
        nicks = list(set(nicks))
        games = list(set(games))

        return render_template('addscore.html', scoretypes = scoretypes, nicks = nicks, games = games)

@app.route("/hiscore")
def hiscore():
    try:
        f = open(HISCORES_FILE, "r")
    except IOError:
        return "No hiscores found!"

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


    # Purkka reversaus? 
    if template_scores[0].scoretype == "points":
        template_scores.reverse()

    if scores2[0].scoretype == "points":
        scores2.reverse()


    template_scores = template_scores[:SCORE_SHOW_NUMBER_MAGIC_VARIABLE]
    scores2 = scores2[:SCORE_SHOW_NUMBER_MAGIC_VARIABLE]


    # Palauta html suoraan: 
    # return string

    # Anna templaten hoitaa hommat: 
    return render_template('hiscore.html', game = template_game, scores = template_scores, 
        game2 = game2, scores2 = scores2)

@app.route("/allscores")
def allscores():
    try:
        f = open(HISCORES_FILE, "r")
    except IOError:
        return "No hiscores found!"

    scores = pickle.load(f)
    games = []
    template_scores = []


    for score in scores:
        games.append(score.game)


    # remove duplicates / get 1 of each game
    games = list(set(games))
    games.sort()


    for game in games:
        aux = []

        for score in scores: 
            if score.game == game:
                aux.append(score)

        aux.sort()
        if aux[0].scoretype == "points": 
            aux.reverse()

        template_scores.append(aux)

    # Template scores sisältää listan scoreja per peli. 


    # Anna templaten hoitaa hommat: 
    return render_template('allscores.html', games = games, scores = template_scores)


if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
