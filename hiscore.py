# -*- conding: utf-8 -*-
from functools import total_ordering
import datetime
import time


@total_ordering
class Hiscore():
    def __init__(self, nick, game, score="0", scoretype="points"): 
        self.nick = nick
        self.game = game
        self.score = score
        self.scoretype = scoretype
        self.date = time.strftime("%d.%m.%Y", time.localtime())

    def __str__(self):
        return self.nick + ", " + self.score + ", " + self.game +"."
        
    def __eq__(self, other):
        if self.scoretype != other.scoretype:
            return False

        elif self.scoretype == "points":
            return (int(self.score) == int(other.score))

        elif self.scoretype == "time":
            return self.score == other.score

        else:
            raise NotImplementedError(" EIOOLE IMPLEMENDOIDU.")

    # def __ne__(self, other):
    #     return not self.__eq__
        
    def __gt__(self, other):
        if self.scoretype != other.scoretype:
            return self.scoretype > other.scoretype

        elif self.scoretype == "points": 
            return (int(self.score) > int(other.score))

        elif self.scoretype == "time":
            try:
                self_time = time.strptime(self.score, "%H:%M:%S")
                other_time = time.strptime(other.score, "%H:%M:%S")
            except ValueError:
                raise ValueError("saatanan saatana")
                # try: 
                #     self_time = time.strptime(self.score, "%M:%S")
                #     other_time = time.strptime(other.score, "%M:%S")
                # except ValueError:
                #     try:
                #         self_time = time.strptime(self.score, "%S")
                #         other_time = time.strptime(other.score, "%S")
                #     except ValueError:
                #         raise ValueError("OPETTELE INPUTTAAMAAN AJAT OIKEIN.", self_time)

            # raise ValueError(self_time  other_time)
            return self_time > other_time

        else:
            raise NotImplementedError(" EIOOLE IMPLEMENDOIDU.")
