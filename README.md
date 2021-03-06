scphabtts
=========

Super cool python highscore and bus time table screen

* Unlikely to be very useful to anyone else or to me. 
* Also, doesn't actually include the high score part.

# how to use 
```python main.py```
its probably wise to run it inside a screen

# How it works
Scphabtts will run a python http server on port 5000 by default
connect to it with ip:5000 or host.local:5000
(if you want to use .local with linux you need to install avahi-daemon)

#Requirements
* you need to install flask
you can do it by ```sudo pip install flask```

* and BeautifulSoup4
```pip install beautifulsoup4```

* if you are running osx you can get pip with
```sudo easy_install pip```
if it doesn't work you can try downloading installe script from
their website: https://pip.pypa.io/en/latest/installing.html#install-or-upgrade-pip

you can also try install python with brew if you can't get those working

# How to actually use it
to use Scpahbtts use following paths with the address 
/hiscore or /newscore /allscores /delscores /regionscores /regionscoreupdate /np or /bussit

* hiscore will display one of the scores at a time and when you load it again
it will show the next one which is usefull if you want to schedule html
template to some kind of DS player such as screenly...

* allscores will show all hiscores saved on the system, usefull if you want to quickly see them all.

* newscore will allow you to add new scores

* delscores will allow you to delete scores if somebody messed up

* regionscoreupdate will allow you to merge multiple hiscores by url

* bussit will fetch data from HSL and format it to usable form without the API

* np is a script for now playing if you are running mopidy

* there's also output /allscoretransfer
which should be used for transfering link for regionscoreupdate
so use this output if you want to merge scores

# More stuff
It's probably good idea to put some sort of backup function to your scores
this means the hiscores.hax file. Crontab and rsync are good options to use.

If you have Scphabtts running on a host and client side you can fetch the scores easily with crontab
with something like this ```*/1 * * * * rsync -vzh user@yourserver:/location/hiscores.hax /home/user/scphabtts/```
this is a one minute cycle

There's a merge function for multiple hiscores if you want to combine multiple hiscore tables to one huge
best of the best hiscore table. Add your additional hiscore locations to /regionscoreupdate

keep in mind that regionscore will combine same nicks so you can't have two people having the same nick
also it will remove any duplicate scores.

#crontabexamples
* backup your hiscores to /var/www where you can also directly read them with other system if you want to

``` */10 * * * * /home/user/copy-scphabtts ```

* the sh file:
``` #!/bin/sh ```

``` cp yourfile.hax /var/www/yourfile.hax ```

* Hiscore dumper will upload your file to dropbox with dropbox_uploader.sh for sharing them
``` */10 * * * * /home/user/hiscores-merge.sh ```

the sh file:
``` #!/bin/sh ```

``` /home/user/Dropbox-Uploader/dropbox_uploader.sh upload /var/www/hiscores.hax /Public/nes/ ```

# Run on boot

* if you want to run the server on boot this might work on crontab -e

``` #@reboot /usr/bin/screen -fa -d -m -S scphabtts $HOME/scphabtts/main.py ```

* there's also file named scphabtts which is a init.d script you can use
open the file for more specs
