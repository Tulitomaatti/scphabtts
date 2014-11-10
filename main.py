# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from hiscore import Hiscore

import pickle

import urllib2
from bs4 import BeautifulSoup

import os
import time

MAGIC_URL = "http://www.omatlahdot.fi/omatlahdot/web?command=embedded&action=view&c=15&o=1&s=1220182"
MAGIC_NUMBER = 1
SCORE_SHOW_NUMBER_MAGIC_VARIABLE = 8

HISCORES_FILE = os.getenv("HOME") + "/scphabtts/hiscores.hax"
HISCORE_FILE = HISCORES_FILE
REGION_FILE_SUFFIX = "/scphabtts/region.hax"
REGION_MEMBERS_FILE = os.getenv("HOME") + REGION_FILE_SUFFIX

REGION_HISCORE_FILE = os.getenv("HOME") + "/scphabtts/region_scores.hax"

HMS_FORMAT = "%H:%M:%S"
MS_FORMAT = "%M:%S"
S_FORMAT = "%S"

app = Flask(__name__)

@app.route("/")
def adsf():
    return "Go to /hiscore or /allscores /delscores /regionscores /regionscoreupdate /np /allscoretransfer or /bussit"

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
                f = open(HISCORE_FILE + ".backup", "rb")
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


@app.route("/regionscoreupdate", methods=['POST', 'GET'])
def region_update():

    region_members = []
    try:
        f = open(REGION_MEMBERS_FILE, "rb")
        for line in f: 
            region_members.append(line)
    except IOError:
        try:
            f = open(REGION_MEMBERS_FILE, "wb")
            f.close()
            f = open(REGION_MEMBERS_FILE, "rb")
        except IOError:
            return "Couldn't read region members, and couldn't even create a new empty list. duh."
    f.close()

    if request.method == 'POST':
        form = request.form

        action = form['action']

        if action == 'add_member':

            f = open(REGION_MEMBERS_FILE, "ab")
            f.write(form['new_member'] + "\n")
            f.close()

            return form['new_member'] + "added to score region."

        elif action == 'update_scores':
            new_scores = []
            for member in region_members:
                current_member_page = urllib2.urlopen(member)


                #hoaly purkka perkelsson purkitettuna
                for line in current_member_page:
                    score_temp = line.split('~')

                    try:
                        if score_temp[3] == 'time':
                            try:
                                time_temp = time.strptime(score_temp[2], "%H h %M min %S sec")
                            except ValueError:
                                try:
                                    time_temp = time.strptime(score_temp[2], "%M min %S sec")
                                except ValueError:
                                    try:
                                        time_temp = time.strptime(score_temp[2], "%S sec")
                                    except ValueError:
                                        raise ValueError("saatanan saatana", score_temp[2])

                            hour = time.struct_time((1900, 1, 1, 1, 0, 0, 0, 1, -1))
                            minute = time.struct_time((1900, 1, 1, 0, 1, 0, 0, 1, -1))

                            if time_temp >= hour:
                                score_temp[2] = time.strftime(HMS_FORMAT, time_temp)
                                if time_temp.tm_hour < 10:
                                    score_temp[2] = score_temp[2][1:]
                            elif time_temp >= minute:
                                score_temp[2] = time.strftime(MS_FORMAT, time_temp)
                                if time_temp.tm_min < 10:
                                    score_temp[2] = score_temp[2][1:]
                            else: 
                                score_temp[2] = time.strftime(S_FORMAT, time_temp)
                                if time_temp.tm_sec < 10:
                                    score_temp[2] = score_temp[2][1:]

                            score_temp[2] = score_temp[2].replace(' 0', ' ')  



                        score_temp[4] = score_temp[4][:-2]
                        hiscore_temp = Hiscore(score_temp[0], score_temp[1], score_temp[2], score_temp[3])
                        hiscore_temp.date = score_temp[4]
                       # hiscore_temp.date = hiscore_temp.date[:-2]


                        

                        new_scores.append(hiscore_temp)

                  


                    except IndexError:
                        if score_temp != ['\n']:
                            raise ValueError("I don't even know what error this error is error")

                # at this point we have read scores from _one site_ to new_scores. 
                # ... just loop until we have ALL THE SCORES MWAHAHAHA. 



            # now we have all the scores.                    

            try:
                f = open(REGION_HISCORE_FILE, 'rb')
                scores = pickle.load(f)
                f.close()
            except IOError:
                scores = []

            for score in new_scores: 
                scores.append(score)

            try: 
                f = open(HISCORE_FILE, 'rb')
                scores_local = pickle.load(f)
                f.close()
            except IOError:
                scores_local = []

            for score in scores_local:
                scores.append(score)

            #remove duplicates: 
            scores_unique = []
            scores = sorted(scores)
            last_score = Hiscore("", "")

            for score in scores:
                if score == last_score:
                    continue
                scores_unique.append(score)
                last_score = score

#            list(set(scores))

            try:
                f = open(REGION_HISCORE_FILE, 'wb')
            except IOError:
                return "couldn't open region hiscore file. uguu."

            pickle.dump(scores_unique, f)
            f.close()



            return "yeaaahhh... ?"

        else:
            return "Unknown action."

    else:


        region_members_string = ""
        for member in region_members:
            region_members_string += member + '\n'

        return render_template('regionscoreupdate.html', members = region_members)




@app.route("/regionscores")
def region_scores():

    try:
        f = open(REGION_HISCORE_FILE, "r")
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





@app.route("/allscoretransfer")
def score_transfer():
        try:
            f = open(HISCORES_FILE, "rb")
        except IOError:
            return "No hiscores found!"

        scores = pickle.load(f)
        f.close()



        # Anna templaten hoitaa hommat: 
        return render_template('allscoretransfer.html', scores = scores)


@app.route("/delscore", methods=['POST', 'GET'])
def hubulboga():

    if request.method == 'POST':

        form = request.form

        try:
            index_of_the_score_to_erase_forever = int(form['score_selection'])
        except KeyError:
            return "Could not extract score index from POSTed form!"

        if (index_of_the_score_to_erase_forever < 0):
            return "LOVE AND PEACE!!! NO DELETIONS!"


        try:
            f = open(HISCORES_FILE, "r")
        except IOError:
            return "No hiscores found!"

        scores = pickle.load(f)
        f.close()

        deleted_score = scores.pop(index_of_the_score_to_erase_forever)


        try:
            f = open(HISCORES_FILE, "wb")
        except IOError: 
            return "AAAAA I CAN'T EVEN OPEN A FILE! "

        try: 
            pickle.dump(scores, f)
        except IOError:
            return "AASDLKdfjss couldn't write the file. lol."

        f.close()

        return "deleted the score: " + str(index_of_the_score_to_erase_forever) + ": " + str(deleted_score)



    else:

        try:
            f = open(HISCORES_FILE, "rb")
        except IOError:
            return "No hiscores found!"

        scores = pickle.load(f)
        f.close()



        # Anna templaten hoitaa hommat: 
        return render_template('delscore.html', scores = scores)




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
