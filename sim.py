#! /usr/bin/env python
#
# python flipdot display simulator


import curses
import SocketServer
import threading
import time

from PIL import Image

import display


RefreshRate = 0.2
sim = None
stdscr = None


class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        data = self.validate(data)
        if data:
            self.update_display(data)

    def validate(self, raw):
        data = [ord(x) for x in raw]
        if data[0] != 0x80:
            print "no start"
            return []
        if data[1] not in (0x81, 0x82, 0x83, 0x84, 0x85, 0x86):
            print "not right command"
            return []
        if data[1] in (0x81, 0x82):
            l = 112
        elif data[1] in (0x83, 0x84):
            l = 28
        elif data[1] in (0x85, 0x86):
            l = 56
        if len(data) != (l + 4):
            print "bad length", len(data)
            return []
        if data[-1] != 0x8F:
            print "no end"
            return []
        return data

    def update_display(self, data):
        address = data[2]
        # if data[1] in (0x82, 0x83, 0x85):
        #     sim.refresh(address)
        body = data[3:-1]
        # print "SIM", address, len(body), list(body)
        sim.update(address, body)


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


def start_server():
    HOST, PORT = "localhost", 9999
    server = ThreadedUDPServer((HOST, PORT), UDPHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()


class DisplaySim(threading.Thread):

    def __init__(self, w, h, panels=None):
        super(DisplaySim, self).__init__()
        self.d = display.Display(w, h, panels)
        self.l = threading.RLock()
        self.frames = 0
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        self.join()

    def run(self):
        while not self._stop.is_set():
            self.frames += 1
            # print '\033c', self.frames
            with self.l:
                self.draw()
            time.sleep(RefreshRate)

    def draw(self):
        px = self.d.im.load()
        w, h = self.d.im.size
        r = w*2+3
        onoff = {True: " *", False: "  "}
        stdscr.addstr(0, 1, "-"*r)
        stdscr.addstr(h+1, 1, "-"*r)
        for y in range(h):
            stdscr.addstr(y+1, 0, "|")
            stdscr.addstr(y+1, r+1, "|")
            for x in range(w):
                v = self.d.px_to_bit(px[x, y])
                stdscr.addstr(y+1, 3+x*2, onoff[v])
        stdscr.refresh()

    def refresh(self, address=None):
        with self.l:
            self.d.reset(address)

    def update(self, address, data):
        # update the internal image from the given list of bytes
        (xs, ys), (w, h) = self.d.panels[address]
        n = Image.new("RGB", (w, h))
        if h is not 7:
            print "H is not 7!!!"
        for x in range(w):
            # get the next byte
            b = data[x]
            for y in range(h):  # note that h should always be 7
                px = b & 0x01
                b = b >> 1
                if px:
                    n.putpixel((x, y), (255, 255, 255))
        with self.l:
            self.d.im.paste(n, (xs, ys))


def init_curses():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()


def stop_curses():
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    sim = DisplaySim(28, 14,
                     panels={
                         2: ((0, 0), (28, 7)),
                         1: ((0, 7), (28, 7)),
                        })
    try:
        init_curses()
        sim.start()
        start_server()
        try:
            while True:
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        sim.stop()
    finally:
        stop_curses()
