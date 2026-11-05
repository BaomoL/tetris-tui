from config import (rotate_clockwise, rotate_counter_clockwise, rotate_one_eighty, rotate_clockwise_backup,
                    move_left, move_right, soft_drop, hard_drop, hold)

from enum import Enum, auto
from keys import pressed
from pynput.keyboard import Key

class Action(Enum):
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    ROTATE_180 = auto()
    LEFT = auto()
    RIGHT = auto()
    SOFT_DROP = auto()
    HARD_DROP = auto()
    HOLD = auto()
    MENU_DOWN = auto()
    MENU_UP = auto()
    MENU_RIGHT = auto()
    MENU_LEFT = auto()
    MENU_ENTER = auto()
    MENU_ESC = auto()

bindings = {
    "move_left": move_left,
    "move_right": move_right,
    "soft_drop": soft_drop,
    "hard_drop": hard_drop,
    "hold": hold,
    "rotate_clockwise": rotate_clockwise,
    "rotate_counter_clockwise": rotate_counter_clockwise,
    "rotate_one_eighty": rotate_one_eighty,
    "rotate_clockwise_backup": rotate_clockwise_backup,
}

default_bindings = dict(bindings)

key_names = {
    Key.up: "Up",
    Key.down: "Down",
    Key.left: "Left",
    Key.right: "Right",
    Key.space: "Space",
    Key.enter: "Enter",
    Key.esc: "Esc",
    Key.tab: "Tab",
    Key.backspace: "Backspace",
    Key.delete: "Delete",
    Key.caps_lock: "Caps Lock",
    Key.shift: "Shift",
    Key.shift_l: "Left Shift",
    Key.shift_r: "Right Shift",
    Key.ctrl: "Ctrl",
    Key.ctrl_l: "Left Ctrl",
    Key.ctrl_r: "Right Ctrl",
    Key.alt: "Alt",
    Key.alt_l: "Left Alt",
    Key.alt_r: "Right Alt",
    Key.cmd: "Cmd",
    Key.cmd_l: "Left Cmd",
    Key.cmd_r: "Right Cmd",
    Key.home: "Home",
    Key.end: "End",
    Key.page_up: "Page Up",
    Key.page_down: "Page Down",
    Key.f1: "F1", Key.f2: "F2", Key.f3: "F3", Key.f4: "F4",
    Key.f5: "F5", Key.f6: "F6", Key.f7: "F7", Key.f8: "F8",
    Key.f9: "F9", Key.f10: "F10", Key.f11: "F11", Key.f12: "F12",
    None: '-'
}

menu = {Key.up: Action.MENU_UP,
        Key.down: Action.MENU_DOWN,
        Key.left: Action.MENU_LEFT,
        Key.right: Action.MENU_RIGHT,
        Key.enter: Action.MENU_ENTER,
        Key.esc: Action.MENU_ESC
        }

actions = {
        "rotate_clockwise": Action.ROTATE_CW,
        "rotate_counter_clockwise": Action.ROTATE_CCW,
        "rotate_one_eighty": Action.ROTATE_180,
        "rotate_clockwise_backup": Action.ROTATE_CW,
        "move_left": Action.LEFT,
        "move_right": Action.RIGHT,
        "soft_drop": Action.SOFT_DROP,
        "hard_drop": Action.HARD_DROP,
        "hold": Action.HOLD,
        }


# p1_bindings = {
#     "move_left": 'a',
#     "move_right": 'd',
#     "soft_drop": 's',
#     "hard_drop": 'c',
#     "hold": Key.shift,
#     "rotate_clockwise": 'r',
#     "rotate_counter_clockwise": 't',
#     "rotate_one_eighty": 'y',
#     "rotate_clockwise_backup": 'f',
# }



# p2_bindings = {
#     "move_left": Key.left,
#     "move_right": Key.right,
#     "soft_drop": Key.down,
#     "hard_drop": Key.space,
#     "hold": 'b',
#     "rotate_clockwise": 'l',
#     "rotate_counter_clockwise": 'j',
#     "rotate_one_eighty": 'i',
#     "rotate_clockwise_backup": ';',
# }
# 

"""test controls"""
p1_bindings = {
    "move_left": move_left,
    "move_right": move_right,
    "soft_drop": soft_drop,
    "hard_drop": hard_drop,
    "hold": hold,
    "rotate_clockwise": rotate_clockwise,
    "rotate_counter_clockwise": rotate_counter_clockwise,
    "rotate_one_eighty": rotate_one_eighty,
    "rotate_clockwise_backup": rotate_clockwise_backup,
}
p2_bindings = {
    "move_left": None,
    "move_right": None,
    "soft_drop": None,
    "hard_drop":None,
    "hold": None,
    "rotate_clockwise": None,
    "rotate_counter_clockwise": None,
    "rotate_one_eighty": None,
    "rotate_clockwise_backup": None,
}

class Controls:

    def __init__(self, game_state, binds=bindings):
        self.last_held = set()
        self.game_state = game_state

        # key binds are based on bindings dictionary
        self.keybinds = {}
        if self.game_state == 'game':
            for name, action in actions.items():
                self.keybinds[binds[name]] = action
        else:
            self.keybinds = menu

        self.read()

    def read(self):

        keys_pressed = set(pressed)

        held_actions = set()

        for key in keys_pressed:
            action = self.keybinds.get(key)
            if action is not None:
                held_actions.add(action)

        new_actions = held_actions - self.last_held

        self.last_held = held_actions

        return new_actions, held_actions

class KeyReader:

    def __init__(self):
        self.last_held = set(pressed)

    def read(self):

        held_actions = set(pressed)

        new_actions = held_actions - self.last_held

        self.last_held = held_actions


        return new_actions