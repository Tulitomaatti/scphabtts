scphabtts
=========

Super cool python highscore and bus time table screen

* Unlikely to be very useful to anyone else or to me. 
* Also, doesn't actually include the high score part.

# how to use (it probably wise to run it inside a screen)
python main.py

Scphabtts will run a http server on port 5000 by default
connect to it with ip:5000 or host.local:5000
(if you want to use .local with linux you need to install avahi-daemon)

to use Scpahbtts use following with the address 
/hiscore or /allscores /delscores /regionscores /regionscoreupdate or /bussit

It's probably good idea to put some sort of backup function to your scores
this means the hiscores.hax file. Crontab and rsync are good options to use.

if you have Scphabtts running on a host and client side you can fetch the scores easily with crontab
with something like this */1 * * * * rsync -vzh user@yourserver:/location/hiscores.hax /home/user/scphabtts/
this is a one minute cycle

there's a merge function for multiple hiscores if you want to combine multiple hiscore tables to one huge
best of the best hiscore table. Add your additional hiscore locations to /regionscoreupdate

keep in mind that regionscore will combine same nicks so you can't have two people having the same nick
also it will remove any duplicate scores.
