import sys
from net import Connection
from canvas import Canvas
from terminal import raw_mode
from match import run_online_match
from keys import listener
from game import Game

if sys.argv[1] == 'host':
    net = Connection('host')
else:
    net = Connection('join', sys.argv[2])

canvas = Canvas(100, 35)


try:
    listener.start()
    with raw_mode():
        run_online_match(canvas, net)

finally:
    canvas.close()
    listener.stop()