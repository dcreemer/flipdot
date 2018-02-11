#! /usr/bin/env python

import sys
import time

from demo import animations
from flipdot import client, display


d = display.Display(28, 14,
                    panels={
                        2: ((0, 0), (28, 7)),
                        1: ((0, 7), (28, 7)),
                    })


def transition(d):
    animations.rand(d)


def mainloop(d):
    animations.display_text(d, "YO!")
    time.sleep(2)
    transition(d)
    animations.blink_text(d, "HI!")
    time.sleep(1)
    transition(d)
    animations.scroll_text(d, "This is scrolled text.", font=animations.SmallFont)
    time.sleep(0.5)
    transition(d)
    d.reset()
    d.send()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "udp":
        d.connect(client.UDPClient("localhost", 9999))
    else:
        d.connect(client.SerialClient('/dev/ttyUSB1'))
    try:
        # intro(d)
        while True:
            mainloop(d)
    finally:
        d.disconnect()


if __name__ == "__main__":
    main()
