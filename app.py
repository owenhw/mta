from nyct_gtfs import NYCTFeed
from datetime import datetime
import math
import os
import sys
from time import sleep



class BoardFeed:
    def __init__(self, key=os.environ['MTA_API_KEY'], line='C', stop='A47'):
        self.key = key
        self.line = line
        self.n_stop = stop.upper()+'N'
        self.s_stop = stop.upper()+'S'
        self.get_arrivals()


    # TODO write a function to get the eta instad of reusing code
    def get_eta(self, n_or_s):
        return None

    def get_arrivals(self):
        self.trains = NYCTFeed(self.line, api_key=self.key).filter_trips(headed_for_stop_id=[self.n_stop, self.s_stop])
        self.n_arrivals = []
        self.s_arrivals = []


        for t in self.trains:
            if t.direction == 'N':
                for s in t.stop_time_updates:
                    if s.stop_id == self.n_stop:
                        self.n_arrivals.append(
                        {'destination': t.headsign_text,
                        'eta': math.floor((s.arrival - datetime.now()).seconds/60)
                        }
                        )

            else:
                for s in t.stop_time_updates:
                    if s.stop_id == self.s_stop:
                        self.s_arrivals.append(
                        {'destination': t.headsign_text,
                        'eta': math.floor((s.arrival - datetime.now()).seconds/60)
                        }
                        )

    def draw(self):
        sys.stdout.flush()
        print('NORTHBOUND', '\n', self.n_arrivals, '\n', 'SOUTHBOUND', '\n', self.s_arrivals, end='\r')



if __name__ == '__main__':
    bf = BoardFeed()
    while True:
        bf.draw()
        sleep(15)
        bf.get_arrivals()
