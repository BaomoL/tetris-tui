import random
from game import Game
from controls import Controls, p1_bindings, p2_bindings
from pynput.keyboard import Key
from keys import pressed
from config import tick_rate, fps
from renderer import render, text
from net import OpponentPOV
import time

def run_match(canvas, game_mode):
    seed = random.randint(0, 1000000)

    game1 = Game(canvas, game_mode, 1, seed)
    game2 = Game(canvas, game_mode, 2, seed)

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

        game1.incoming.extend(game2.outgoing)
        game2.incoming.extend(game1.outgoing)

        game1.outgoing = []
        game2.outgoing = []

        time.sleep(1/tick_rate)

        if now - last_render >= 1/fps:
            buffer = canvas.blank_canvas()
            render(game1, game1.board, buffer, 0)
            render(game2, game2.board, buffer, 50)
            canvas.load(buffer)
            last_render = now

    return game1, game2

# run match but with someone online

def run_online_match(canvas, net, game_seed):

    if net.mode == 'host':
        player_num = 1
    else:
        player_num = 2

    my_game = Game(canvas, ("Versus", None, None, None), player_num=player_num, seed= game_seed)

    my_controls = Controls("game")

    my_game.begin()

    last_render = time.perf_counter()

    last_send = time.perf_counter()

    other_player_lost = False

    while my_game.running and not other_player_lost:

        if Key.esc in pressed:
            my_game.lost = True
            my_game.running = False

        new_presses, held_presses = my_controls.read()

        now = time.perf_counter()

        my_game.tick(new_presses, held_presses, now)

        while net.attacks:
            my_game.incoming.append(net.attacks.pop(0))

        if now - last_render >= 1/fps:
            buffer = canvas.blank_canvas()
            render(my_game, my_game.board, buffer, 0)

            # ensure game is still connected before sending
            if now - last_send >= 1/20:
                try:
                    net.send(my_game.snapshot())
                except OSError:
                    net.connected = False
                last_send = now

                my_game.outgoing = []

            if net.latest is not None:
                op_pov = OpponentPOV(net.latest)
                render(op_pov, op_pov.board, buffer, 50)

            # show disconnect message
            if not net.connected:
                text(buffer, 12, 65, "Disconnected!", (255, 80, 80))
                
            canvas.load(buffer)
            last_render = now

        if net.latest is not None and net.latest['lost']:
            other_player_lost = True

        time.sleep(1/tick_rate)

    try:
        final_snapshot = my_game.snapshot()
        final_snapshot['final'] = True
        net.send(final_snapshot)
    except OSError:
        net.connected = False

    return my_game

