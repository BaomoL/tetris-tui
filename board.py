# board class represents current active board

class Board:

    empty_row = ['.'] + [None] * 10 + ['.']
    floor_row = ['.'] * 12

    # create 22x12 board, '.'s represent borders and Nones represent empty space

    def __init__(self):
        self.grid = [list(Board.empty_row) for _ in range(21)] + [list(Board.floor_row)]
        self.placed_pieces = 0

    # # gauge how far a piece can drop

    def drop_distance(self, piece):

        distance = 1

        while self.is_valid(piece, dy = distance):
            distance += 1

        return distance - 1

    # permanently append the piece to the real board

    def lock_piece(self, piece):

        for piece_y in range(len(piece.shape)):
            for piece_x in range(len(piece.shape[piece_y])):
                
                board_x = piece.x + piece_x
                board_y = piece.y + piece_y

                if piece.shape[piece_y][piece_x]:
                    self.grid[board_y][board_x] = piece.shape[piece_y][piece_x]

        self.placed_pieces += 1

    # check if a clear is a perfect clear (clears entire board)

    def perfect_clear(self):

        return all(not cell for row in self.grid[:-1] for cell in row[1:-1])

    # checks if any given move is valid (allows a proposed shape if a spin is involved <- used for kick positions)

    def is_valid(self, piece, proposed = None, dx=0, dy=0):

        shape = proposed if proposed is not None else piece.shape

        for piece_y in range(len(shape)):
            for piece_x in range(len(shape[piece_y])):
                if shape[piece_y][piece_x]:

                    board_x = piece.x + piece_x + dx
                    board_y = piece.y + piece_y + dy

                    if not (0 <= board_x < len(self.grid[0]) and
                            0 <= board_y < len(self.grid)):
                        return False

                    if self.grid[board_y][board_x]:
                        return False
        return True

    # check of conditions for a t-spin is met: last successful move was a spin AND at least 3 corners are covered

    def detect_t_spin(self, piece):
        corners_covered = 0
        if piece.type == 't':
            for x in [0, 2]:
                for y in [0, 2]:
                    if self.grid[piece.y + y][piece.x + x]:
                        corners_covered += 1
    
        if piece.last_move == 'rotate' and corners_covered >= 3:

            return True

        return False

    # check and clear rows that are filled

    def clear_rows(self):

        cleared = 0
        cheese_cleared = 0

        for y in range(0, len(self.grid) - 1):
            if all(x for x in self.grid[y][1:-1]):
                if any(x == 'g' for x in self.grid[y][1:-1]):
                    cheese_cleared += 1
                self.grid.pop(y)
                self.grid.insert(0, list(Board.empty_row))
                cleared += 1

        return cleared, cheese_cleared

    def add_garbage(self, amount, hole):
        garbage_line = list('.gggggggggg.')
        garbage_line[hole] = None
        for i in range(amount):
            self.grid.pop(0)
            self.grid.insert(((len(self.grid)-1)-i), list(garbage_line))


