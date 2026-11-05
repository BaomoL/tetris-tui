import socket, json, threading
from config import PORT
from board import Board
from pieces import Piece

class Connection:

    def __init__(self, mode, ip=None):

        # create socket

        if mode == "host":
            self.server = socket.socket()
            self.server.bind(("0.0.0.0", PORT))
            self.server.listen()
            self.conn, self.addr = self.server.accept()
        else:
            self.conn = socket.socket()
            self.conn.connect((ip, PORT))

            # need to assign somethign to server to avoid crashing
            self.server = None

        self.connected = True
        self.latest = None

        # check attacks separately to avoid data loss

        self.attacks = []

        threading.Thread(target=self.receive_loop, daemon=True).start()


    def send(self, data):

        # send current data as json

        self.conn.sendall((json.dumps(data) + "\n").encode())

        # receive data; receive as json and then parse

    def receive_loop(self):
        # save the file
        incoming_json = self.conn.makefile("r")

        while True:
            line = incoming_json.readline()
            if line == "":
                self.connected = False
                return
            latest = json.loads(line) 
            self.latest = latest

            # grab attacks with dictonary key; default to []

            self.attacks.extend(latest.get("attacks", []))

    def close(self):
         if self.server:
            self.conn.close()

class OpponentPOV:

    # recreate the board using the snapshot taken using snap

    def __init__(self, snap):
        self.board = Board()
        self.board.grid = snap["grid"]
        self.board.placed_pieces = snap["placed_pieces"]

        piece = snap["piece"]
        self.active_piece = Piece(piece["type"], piece["x"], piece["y"])
        self.active_piece.shape = piece["shape"]

        self.held_piece = snap["held"]
        self.pieces = snap["queue"]
        self.incoming = snap["incoming"]
        self.mode = snap["mode"]
        self.player_num = snap["player_num"]
        self.total_attacks = snap["total_attacks"]
        self.elapsed_time = snap["elapsed_time"]
        self.combo = snap["combo"]
        self.last_clear_type = snap["last_clear_type"]
