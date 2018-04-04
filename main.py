import chess

"""
TODO:

- Make a more specific TODO list. 

- Implement UCI. Essentially, this is the engine and it will
take input from the GUI for commands like "isready" and "uci" etc.
in order to set itself up for play.

- Actually write a working algorithm.

- Hook it up to a GUI (this works with the UCI thing)

"""

#Setup Main Board
board = chess.Board()


#Choose a move
def AI_move(board):
	m = ""
	for move in board.legal_moves: #So this is weird - it's non-subscriptable but it is iterable. Need to figure out how to utilise it better.
		m = chess.Move.from_uci(str(move)) #Can't find any documentation on it either.
		break
	board.push(m)
	print(board)
	print()
print(board)


#######TEMPORARY SECTION - USER INPUT SO WE CAN INTERACT WITH THE ENGINE, WILL 
#######DISABLE WHEN WE NEED TO CONVERT TO UCI#################
end = False

def input_move(board):
	move = input("Input move (UCI 4 char str ONLY):\n")
	move = chess.Move.from_uci(move)
	board.push(move)
	print(board)
	print()

def temp_game_loop(end, board):
	
	while not end:
		if board.turn:
			input_move(board)
		else:
			AI_move(board)

if __name__ == "__main__":
	temp_game_loop(False, board)