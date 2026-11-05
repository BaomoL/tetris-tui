from pieces import Piece

# function for converting time to time format

def format_time(seconds):

    minutes, seconds = divmod(int(seconds), 60)

    return f'{minutes:02d}:{seconds:02d}'

# convert regular characters into blocks

def draw_block(canvas, row, col, char, offset=0):
    canvas[row][col*2 + offset] = char
    canvas[row][col*2+1 + offset] = char

# append text into canvas

def text(canvas, row, col, text, fcolor = None, bcolor = None):
    column = col
    for letter in list(text):

        # ensure no index error by only printing letters within borders of canvas 
        if column > len(canvas[0]) - 1 or row > len(canvas) - 1:
            break
        canvas[row][column] = (letter, fcolor, bcolor)
        column+=1

def display_menu(canvas, lines, title, selected):

    new_buffer = canvas.blank_canvas()

    row = 4

    # draw menu title

    text(new_buffer, row-2, 4, title, (255,255,255))

    # draw items; highlight if highlight is True

    for item_position, (item, highlight) in enumerate(lines):

        # space out settings one extra
        if item == "Start":
            text(new_buffer, row, 4, '---------', (255,255,255))
            row += 1

        if item in ("Sprint", "Ultra", "Cheese Race", "Settings", "Multiplayer"):
            text(new_buffer, row, 16, '›', (255,255,255))
        
        if highlight:
            text(new_buffer, row, 4, item, (0,0,0), (255,255,255))
        else:
            text(new_buffer, row, 4, item, (255,255,255))
        if item_position == selected:
            text(new_buffer, row, 2, '>', (255,255,255))

        row += 1

    canvas.load(new_buffer)

def display_results(game, buffer, x_offset):
    if game.mode in ("Marathon", "Hardcore", "Sprint", "Ultra", "Cheese Race"):
        if game.mode == 'Sprint':
            text(buffer, 3, 3+x_offset, f'{game.mode} | {game.total_lines}/{game.sprint}', (255,255,255))

        if game.mode == 'Cheese Race':
            text(buffer, 3, 3+x_offset, f'{game.mode} | {game.cheese_cleared}/{game.cheese}', (255,255,255))

        if game.mode in ('Hardcore', 'Marathon'):
            text(buffer, 3, 3+x_offset, f'{game.mode} | Level: {game.level}', (255,255,255))

        if game.mode == 'Ultra':
            text(buffer, 3, 3+x_offset, f'{game.mode} | {format_time(game.elapsed_time)}/{format_time(game.ultra)}', (255,255,255))

        text(buffer, 4, 3+x_offset, f'Score: {int(game.score)}', (255,255,255))
        text(buffer, 5, 3+x_offset, f'Elapsed Time: {format_time(game.elapsed_time)}', (255,255,255))
        text(buffer, 6, 3+x_offset, f'Pieces Placed: {game.board.placed_pieces}', (255,255,255))
        text(buffer, 7, 3+x_offset, f'Lines Cleared: {game.total_lines}', (255,255,255))
        text(buffer, 8, 3+x_offset, f'Piece Per Second: {round(game.board.placed_pieces/game.elapsed_time, 2)}', (255,255,255))

        text(buffer, 10, 3+x_offset, 'Press Enter to play again', (255,255,255))
        text(buffer, 11, 3+x_offset, 'Press Esc to return to menu', (255,255,255))
    else:
        text(buffer, 5, 3+x_offset, f'Total Attack: {game.total_attacks}', (255,255,255))
        if game.elapsed_time > 0:
            text(buffer, 6, 3+x_offset, f'Attacks Per Minute: {round(game.total_attacks/(game.elapsed_time/60), 2)}', (255,255,255))
        text(buffer, 7, 3+x_offset, f'Elapsed Time: {format_time(game.elapsed_time)}', (255,255,255))
        text(buffer, 8, 3+x_offset, f'Pieces Placed: {game.board.placed_pieces}', (255,255,255))
        text(buffer, 9, 3+x_offset, f'Lines Cleared: {game.total_lines}', (255,255,255))
        text(buffer, 10, 3+x_offset, f'Piece Per Second: {round(game.board.placed_pieces/game.elapsed_time, 2)}', (255,255,255))
    
def display_multiplayer_results(games, buffer):
    winner = 1 if games[0].lost == False else 2
    text(buffer, 3, 3, f'Winner: Player {winner}', (255,255,255))
    text(buffer, 12, 3, 'Press Enter to play again', (255,255,255))
    text(buffer, 13, 3, 'Press Esc to return to menu', (255,255,255))
    
def render(game, board, buffer, x_offset=0):

    # only puts a color when truth value

    for row in range(2):
            for column in range(1, len(board.grid[row])-1):
                if board.grid[row][column]:
                    draw_block(buffer, row, column, (' ', None, Piece.piece_colors[board.grid[row][column]]), 10+x_offset)

    for row in range(2, len(board.grid)):
        for column in range(len(board.grid[row])):
            if board.grid[row][column]:
                draw_block(buffer, row, column, (' ', None, Piece.piece_colors[board.grid[row][column]]), 10+x_offset)

    # ghost piece
    ghost_y = game.active_piece.y

    ghost_y += board.drop_distance(game.active_piece)
        
    for y in range(len(game.active_piece.shape)):
        for x in range(len(game.active_piece.shape[y])):
            if game.active_piece.shape[y][x]:
                draw_block(buffer, ghost_y+y, game.active_piece.x + x, ('░', game.active_piece.color, None), 10+x_offset)

    # draw piece

    for piece_y in range(len(game.active_piece.shape)):

        for piece_x in range(len(game.active_piece.shape[piece_y])):
            
            board_x = game.active_piece.x + piece_x
            board_y = game.active_piece.y + piece_y
            if game.active_piece.shape[piece_y][piece_x]:
                draw_block(buffer, board_y, board_x, (' ', None, game.active_piece.color), 10+x_offset)

    # draw held piece

    if game.held_piece:
        piece = Piece.shapes[game.held_piece]
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    draw_block(buffer, 3+row, col, (' ', None, Piece.piece_colors[game.held_piece]), x_offset)

    # draw queue

    offset = 3

    for piece in game.pieces[:-6:-1]:
        piece_shape = Piece.shapes[piece]
        for row in range(len(piece_shape)):
            for col in range(len(piece_shape[row])):
                if piece_shape[row][col]:
                    draw_block(buffer, offset+row, col+18, (' ', None, Piece.piece_colors[piece]), x_offset)
        offset += (len(piece_shape) +1)

    # draw incoming attacks bar

    total_incoming_attacks = sum(game.incoming)
    for i in range(total_incoming_attacks):
        if i < 20:
            text(buffer, 20-i, 9+x_offset, ' ', None, (255, 90, 40))

    text(buffer, 1, 2+x_offset, 'HOLD', (255,255,255))
    text(buffer, 1, 36+x_offset, 'NEXT', (255,255,255))

    if game.mode == 'Sprint':
        text(buffer, 23, 10+x_offset, f'{game.mode} | {game.total_lines}/{game.sprint}', (255,255,255))

    if game.mode in ('Hardcore', 'Marathon'):
        text(buffer, 23, 10+x_offset, f'{game.mode} | Level: {game.level}', (255,255,255))

    if game.mode == 'Ultra':
        text(buffer, 23, 10+x_offset, f'{game.mode} | {format_time(game.elapsed_time)}/{format_time(game.ultra)}', (255,255,255))

    if game.mode == 'Cheese Race':
        text(buffer, 23, 10+x_offset, f'{game.mode} | {game.cheese_cleared}/{game.cheese}', (255,255,255))

    if game.mode == 'Versus':
        text(buffer, 23, 10+x_offset, f'{game.mode} | Player {game.player_num}', (255,255,255))        
        text(buffer, 24, 10+x_offset, f'Total Attack: {game.total_attacks}', (255,255,255))
        text(buffer, 25, 10+x_offset, f'Attacks Per Minute: {round(game.total_attacks/(game.elapsed_time/60), 2)}', (255,255,255))
        y = 1
    else:
        text(buffer, 24, 10+x_offset, f'Score: {int(game.score)}', (255,255,255))
        y = 0

    text(buffer, 25+y, 10+x_offset, f'Elapsed Time: {format_time(game.elapsed_time)}', (255,255,255))
    text(buffer, 26+y, 10+x_offset, f'Combo: {game.combo}', (255,255,255))
    text(buffer, 27+y, 10+x_offset, f'Placed: {board.placed_pieces}', (255,255,255))

    if game.elapsed_time > 0:
        text(buffer, 28+y, 10+x_offset, f'PPS: {round(board.placed_pieces/game.elapsed_time, 2)}', (255,255,255))

    if game.last_clear_type:
        text(buffer, 29+y, 10+x_offset, game.last_clear_type, (255,255,255))
    