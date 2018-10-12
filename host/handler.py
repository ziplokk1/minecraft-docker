#!/bin/python
from __future__ import print_function

import subprocess

import sys
import re
import threading
import time
import signal


class LineReader(threading.Thread):

    def __init__(self, feed=sys.stdin):
        super(LineReader, self).__init__()
        self.daemon = True
        self.feed = feed
        self.players = 0
        self.stopped = False
        self.stopping = False

    def player_did_join(self, line):
        ptn = re.compile(r'.*?INFO\]:\s(.*?)\sjoined the game')
        groups = ptn.findall(line)
        if groups:
            return groups[0]

    def player_did_leave(self, line):
        ptn = re.compile(r'.*?INFO\]:\s(.*?)\sleft the game')
        groups = ptn.findall(line)
        if groups:
            return groups[0]

    def parse_line(self, line):
        p_joined = self.player_did_join(line)
        if p_joined:
            self.players += 1

        p_left = self.player_did_leave(line)
        if p_left:
            self.players -= 1

    def run(self):
        # java -Xmx1024M -Xms1024M -jar server.jar nogui
        process = subprocess.Popen(['java', '-Xmx4G', '-Xms4G', '-jar', 'server.jar', 'nogui'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            if line:
                line = line.strip()
                print(line)
                self.parse_line(line)
                if self.stopped:
                    if not self.stopping:
                        process.send_signal(signal.SIGKILL)
                        self.stopping = True
        process.poll()

    def stop(self):
        self.stopped = True


def main():
    reader = LineReader()
    reader.start()
    num_active = reader.players
    times_inactive = 0
    while True:
        print('active_players={}'.format(num_active))
        if num_active == 0:
            times_inactive += 1
        else:
            times_inactive = 0
        if times_inactive == 6:
            print('two minutes until shutdown')
        if times_inactive == 8:
            print('one minute until shutdown')
        if times_inactive == 4:  # 5 minutes of inactivity
            print('shutting down')
            break
        time.sleep(30)
        num_active = reader.players
    reader.stop()


if __name__ == '__main__':
    main()
