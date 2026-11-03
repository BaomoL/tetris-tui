import time
from pynput.keyboard import Key
from keys import pressed
from renderer import display_menu, display_results
from controls import Controls, Action, bindings, key_names, default_bindings
from renderer import format_time

class Setting:

    def __init__(self, control_name):
        self.name = control_name

page = {
    'TUI Tetris': 
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
        
        "Quit": None}
}
def results_menu(canvas, game):
    display_results(canvas, game)

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
    pages = [page["TUI Tetris"]]

    # track current page label using stack
    page_labels =["TUI Tetris"]

    # chosen includes all selected choices
    # default game_mode to avoid crashing

    chosen = {'TUI Tetris': "Marathon"}

    game_mode = ("Marathon", None, None, None)

    waiting_for = None  
    
    while True:

        new_actions, held_actions = inputs.read()

        current_options = list(pages[-1])

        options_num = len(current_options)

        current_page_pointer = pages[-1]

        current_page_label = page_labels[-1]

        selected_option_pointer = current_page_pointer[current_options[selected]]

        selected_option_label = current_options[selected]

        if Action.MENU_DOWN in new_actions:
            selected = (selected +1) % options_num

        if Action.MENU_UP in new_actions:
            selected = (selected - 1) % options_num

        if Action.MENU_RIGHT in new_actions:
            if isinstance(selected_option_pointer, dict):
                pages.append(selected_option_pointer)
                selected = 0
                page_labels.append(selected_option_label)

        if Action.MENU_LEFT in new_actions or Action.MENU_ESC in new_actions:
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
                if current_page_label != "TUI Tetris":
                    chosen["TUI Tetris"] = current_page_label

            # reset controls
            if selected_option_label == "Reset":
                bindings.clear()
                bindings.update(default_bindings)

            elif isinstance(selected_option_pointer, Setting):
                waiting_for = selected_option_pointer.name
    
            # start game
            if selected_option_label == "Start":
                return game_mode

            # quit game
            if selected_option_label == "Quit":
                return None

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
            elif page_labels[-1] == "TUI Tetris":
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
            
        display_menu(canvas, lines, current_page_label, selected)

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