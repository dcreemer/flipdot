#! /usr/bin/env python
#
# panel.py
#

#
# Abstraction for a single AlphaZeta Flip-Dot panel
#


class Panel(object):

    def __init__(self, sid, w, h):
        self.id = sid
        self.size = (w, h)
