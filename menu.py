import time
from pynput.keyboard import Key
from keys import pressed
from renderer import display_menu, display_results, display_multiplayer_results, display_waiting_to_start
from controls import Controls, Action, bindings, key_names, default_bindings, KeyReader
from renderer import format_time
from net import get_local_ip

class Setting:

    def __init__(self, control_name):
        self.name = control_name

page = {
    'TUI Tetris: Single Player': 
        {"Marathon": ("Marathon", None, None, None),

        "Hardcore": ("Hardcore", None, None, None),

        "Sprint": {
            "20 Lines": ("Sprint", 20, None, None),
            "40 Lines": ("Sprint", 40, None, None),
            "100 Lines": ("Sprint", 100, None, None),
        },

        "Ultra": {
            "1 Minute": ("Ultra", None, 60, None),
            "2 Minutes": ("Ultra", None, 120, None),
            "5 Minutes": ("Ultra", None, 300, None),
        },

        "Cheese Race": {
            "10 Lines": ("Cheese Race", None, None, 10),
            "20 Lines": ("Cheese Race", None, None, 20),
            "100 Lines": ("Cheese Race", None, None, 100)
            },

        "Start": True,

        "Settings": {
            "Rotate C": Setting("rotate_clockwise"),
            "Rotate CC": Setting("rotate_counter_clockwise"),
            "Rotate 180": Setting("rotate_one_eighty"),
            "Move Left": Setting("move_left"),
            "Move Right": Setting("move_right"),
            "Soft Drop": Setting("soft_drop"),
            "Hard Drop": Setting("hard_drop"),
            "Hold": Setting("hold"),
            "Rotate C (Backup)": Setting("rotate_clockwise_backup"),
            "Reset": "reset"
        },

        "Multiplayer": 'switch',
        
        "Quit": None
        },

        "TUI Tetris: Multiplayer": {

        "Local": "local",
        "Join": "join",
        "Host": "host",

        "Start": True,

        "Settings": {
            "Rotate C": Setting("rotate_clockwise"),
            "Rotate CC": Setting("rotate_counter_clockwise"),
            "Rotate 180": Setting("rotate_one_eighty"),
            "Move Left": Setting("move_left"),
            "Move Right": Setting("move_right"),
            "Soft Drop": Setting("soft_drop"),
            "Hard Drop": Setting("hard_drop"),
            "Hold": Setting("hold"),
            "Rotate C (Backup)": Setting("rotate_clockwise_backup"),
            "Reset": "reset"
        },

        "Single Player": 'switch',
        
        "Quit": None}
}

def results_menu(canvas, games):

    buffer = canvas.blank_canvas()
    for i, game in enumerate(games):

        display_results(game, buffer, 50 * i)

    if games[0].mode == "Versus":
        display_multiplayer_results(games, buffer)

    canvas.load(buffer)

    inputs = Controls('menu')

    while True:
        new_actions, held_actions = inputs.read()

        if Action.MENU_ENTER in new_actions:
            return False
        if Action.MENU_ESC in new_actions:
            return True

        time.sleep(0.01)


def selection_menu(canvas):

    inputs = Controls('menu')
    
    selected = 0

    # track current page using stack
    pages = [page["TUI Tetris: Single Player"]]

    # track current page label using stack
    page_labels =["TUI Tetris: Single Player"]

    # chosen includes all selected choices
    # default game_mode to avoid crashing

    chosen = {"TUI Tetris: Single Player": "Marathon"}

    game_mode = ("Marathon", None, None, None)

    waiting_for = None  

    selected_multiplayer_option = 0
    network_row = ("Local", "Join", "Host")

    player_ip = "No Network Connection"

    entered_ip = ''

    multiplayer_type = ()

    keyboard_input = KeyReader()
    
    while True:

        new_actions, held_actions = inputs.read()

        current_options = list(pages[-1])

        current_page_pointer = pages[-1]

        current_page_label = page_labels[-1]

        options_num = len(current_options)

        selected_option_pointer = current_page_pointer[current_options[selected]]

        selected_option_label = current_options[selected]

        # only get ip once

        if selected_multiplayer_option == 2 and player_ip == "No Network Connection":
            player_ip = get_local_ip()

        if selected_multiplayer_option == 2:
            multiplayer_type = ('host',)

        if selected_multiplayer_option == 1:
            if entered_ip != '':
                multiplayer_type = ('join', entered_ip)

        if selected_multiplayer_option == 0:
            multiplayer_type = ()

        # for typing in ip

        if selected_multiplayer_option == 1:

            for key in keyboard_input.read():
                if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.') and len(entered_ip) <15:
                    entered_ip += key

                elif key == Key.backspace and len(entered_ip) > 0:
                    entered_ip= entered_ip[:-1]

        if Action.MENU_DOWN in new_actions:
            if selected_option_label in network_row:
                selected = 3
            else:
                selected = (selected +1) % options_num

        if Action.MENU_UP in new_actions:
            if selected_option_label in network_row:
                selected = len(current_options) - 1
            else:
                selected = (selected - 1) % options_num

            if current_options[selected] in network_row:
                selected = 0

        if Action.MENU_RIGHT in new_actions:
            if selected_option_label in network_row:
                selected_multiplayer_option = (selected_multiplayer_option + 1) % 3

            if isinstance(selected_option_pointer, dict):
                pages.append(selected_option_pointer)
                selected = 0
                page_labels.append(selected_option_label)

        if Action.MENU_LEFT in new_actions or Action.MENU_ESC in new_actions:

            if Action.MENU_LEFT in new_actions and selected_option_label in network_row:
                selected_multiplayer_option = (selected_multiplayer_option - 1) % 3

            if len(pages) > 1:
                pages.pop()
                page_labels.pop()
                if selected > len(list(pages[-1])) -1:
                    selected = len(list(pages[-1])) -1

        if Action.MENU_ENTER in new_actions:

            # acts like left arrow if label contains more options
            if isinstance(selected_option_pointer, dict):
                pages.append(selected_option_pointer)
                selected = 0
                page_labels.append(selected_option_label)

            if isinstance(selected_option_pointer, tuple):
                # put selected option into dictionary
                chosen[current_page_label] = selected_option_label

                # tuple = game_mode
                game_mode = selected_option_pointer
                if current_page_label != "TUI Tetris: Single Player":
                    chosen["TUI Tetris: Single Player"] = current_page_label

            # reset controls
            if selected_option_label == "Reset":
                bindings.clear()
                bindings.update(default_bindings)

            elif isinstance(selected_option_pointer, Setting):
                waiting_for = selected_option_pointer.name
    
            # start game
            if selected_option_label == "Start":
                return game_mode, multiplayer_type

            # toggle multiplayer
            if selected_option_label == "Multiplayer":
                page_labels =["TUI Tetris: Multiplayer"]
                pages = [page["TUI Tetris: Multiplayer"]]
                selected_multiplayer_option = 0
                chosen = {}
                selected = 0
                game_mode = ("Versus", None, None, None)

            elif selected_option_label == "Single Player":
                page_labels =["TUI Tetris: Single Player"]
                pages = [page["TUI Tetris: Single Player"]]
                chosen = {"TUI Tetris: Single Player": "Marathon"}
                game_mode = ("Marathon", None, None, None)
                selected = 0

            # quit game
            if selected_option_label == "Quit":
                return None, None

        lines = []

        for line in current_options:

            line_pointer = current_page_pointer[line]

            if isinstance(line_pointer, Setting):
                if line_pointer.name == waiting_for:
                    lines.append((f'{line:<20} Press a key', True))
                else:
                    # either show keybind name or show keybind
                    key = bindings[line_pointer.name]
                    lines.append((f'{line:<20} {key_names[key] if key in key_names else key}', False))
            elif page_labels[-1] == "TUI Tetris: Single Player":
                if game_mode[0] == "Sprint" and line == "Sprint":
                    lines.append((f'{line}: {game_mode[1]}', line in chosen.values()))

                elif game_mode[0] == "Ultra" and line == "Ultra":
                    lines.append((f'{line}: {format_time(game_mode[2])}', line in chosen.values()))

                elif game_mode[0] == "Cheese Race" and line == "Cheese Race":
                    lines.append((f'{line}: {game_mode[3]}', line in chosen.values()))

                else:
                    lines.append((line, line in chosen.values()))
            else:
                    lines.append((line, line in chosen.values()))
            
        display_menu(canvas, lines, current_page_label, selected, network_row[selected_multiplayer_option], player_ip, entered_ip)

        # get last held keys
        last_held = set(pressed)

        while waiting_for:

            # look for new keys
            new_press = set(pressed) - last_held

            if new_press:
                new_key = list(new_press)[0]
                if new_key == Key.esc:
                    waiting_for = None
                    break
                elif new_key in bindings.values():

                    # make sure binds don't conflict
                    for bind in bindings:
                        if bindings[bind] == new_key:
                            bindings[bind] = None
                    bindings[waiting_for] = new_key
                    waiting_for = None
                    break

                else:
                    bindings[waiting_for] = new_key
                    waiting_for = None
                    break

            time.sleep(0.01)

        inputs.read()

        time.sleep(0.01)

def waiting_screen(canvas):
    x = True
    while x:
        display_waiting_to_start(canvas)
        if Key.enter in pressed:
            x = False
        time.sleep(0.01)