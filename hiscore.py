# -*- conding: utf-8 -*-
from functools import total_ordering
import datetime
import time

HMS_FORMAT = "%H h %M min %S sec"
MS_FORMAT = "%M min %S sec"
S_FORMAT = "%S sec"

@total_ordering
class Hiscore():
    def __init__(self, nick, game, score="0", scoretype="points"): 
        self.nick = nick
        self.game = game
        self.score = score
        self.scoretype = scoretype
        self.date = time.strftime("%d.%m.%Y", time.localtime())

        if self.scoretype == "time":
            try:
                scoretime = time.strptime(self.score, "%H:%M:%S")
            except ValueError:
                try:
                    scoretime = time.strptime(self.score, "%M:%S")
                except ValueError:
                    try:
                        scoretime = time.strptime(self.score, "%S")
                    except ValueError:
                        raise ValueError("saatanan saatana", self.score)

            hour = time.struct_time((1900, 1, 1, 1, 0, 0, 0, 1, -1))
            minute = time.struct_time((1900, 1, 1, 0, 1, 0, 0, 1, -1))

            if scoretime >= hour:
                self.score = time.strftime(HMS_FORMAT, scoretime)
                if scoretime.tm_hour < 10:
                    self.score = self.score[1:]
            elif scoretime >= minute:
                self.score = time.strftime(MS_FORMAT, scoretime)
                if scoretime.tm_min < 10:
                    self.score = self.score[1:]
            else: 
                self.score = time.strftime(S_FORMAT, scoretime)
                if scoretime.tm_sec < 10:
                    self.score = self.score[1:]

            self.score = self.score.replace(' 0', ' ')            




    def __str__(self):
        return self.nick + ", " + self.score + " " + self.scoretype + ", " + self.game +"."
        
    def __eq__(self, other):
        if self.scoretype != other.scoretype:
            return False

        elif self.scoretype == "points":
            try:
                return (int(self.score) == int(other.score))
            except ValueError:
                return self.score == other.score

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
            try:
                return (int(self.score) > int(other.score))
            except ValueError:
                # HAX REVERSE ORDER
                return self.score < other.score

        elif self.scoretype == "time":
            try:
                self_time = time.strptime(self.score, HMS_FORMAT)
            except ValueError:
                try:
                    self_time = time.strptime(self.score, MS_FORMAT)
                except ValueError:
                    try:
                        self_time = time.strptime(self.score, S_FORMAT)
                    except ValueError:
                        raise ValueError("saatanan saatana", self_time)

            try:
                other_time = time.strptime(other.score, HMS_FORMAT)
            except ValueError:
                try:
                    other_time = time.strptime(other.score, MS_FORMAT)
                except ValueError:
                    try:
                        self_time = time.strptime(other.score, S_FORMAT)
                    except ValueError:
                        raise ValueError("saatanan saatana", other_time)
            # raise ValueError(self_time  other_time)
            return self_time > other_time

        else:
            raise NotImplementedError(" EIOOLE IMPLEMENDOIDU.")
