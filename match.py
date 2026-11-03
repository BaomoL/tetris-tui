import random
from game import Game
from controls import Controls, p1_bindings, p2_bindings
from pynput.keyboard import Key
from keys import pressed
from config import tick_rate, fps
from renderer import render
import time



def run_match(canvas, game_mode):
    seed = random.randint(0, 1000000)

    game1 = Game(canvas, game_mode, seed)
    game2 = Game(canvas, game_mode, seed)

    p1_controls = Controls('game', p1_bindings)
    p2_controls = Controls('game', p2_bindings)

    game1.begin()
    game2.begin()

    now = time.perf_counter()

    last_render = now

    while game1.running and game2.running:

        if Key.esc in pressed:
            game1.running = False
            game2.running = False

        # read both controls

        p1_new, p1_held = p1_controls.read()
        p2_new, p2_held = p2_controls.read()

        now = time.perf_counter()

        game1.tick(p1_new, p1_held, now)
        game2.tick(p2_new, p2_held, now)

        time.sleep(1/tick_rate)

        if now - last_render >= 1/fps:
            buffer = canvas.blank_canvas()
            render(game1, game1.board, buffer, 0)
            render(game2, game2.board, buffer, 50)
            canvas.load(buffer)
            last_render = now

    return game1, game2