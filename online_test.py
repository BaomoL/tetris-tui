import sys
from net import Connection
from canvas import Canvas
from terminal import raw_mode
from match import run_online_match
from keys import listener
import random


if sys.argv[1] == 'host':
    net = Connection('host')
else:
    net = Connection('join', sys.argv[2])

canvas = Canvas(100, 35)


try:
    listener.start()
    with raw_mode():
        seed = random.randint(1, 100000)
        run_online_match(canvas, net, seed)

finally:
    canvas.close()
    listener.stop()
    net.close()