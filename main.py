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

# Setup Main Board
board = chess.Board()

PIECE_VALUES = {
	"p": 10,
	"b": 30,
	"n": 30,
	"r": 50,
	"q": 90,
	"k": 31337,
	"P": -10,
	"B": -30,
	"N": -30,
	"R": -50,
	"Q": -90,
	"K": -31337,
}

# Choose a move
def AI_move(board):
	m = ""
	bestmove = None
	bestscore = -999999

	for move in board.legal_moves: 
		board.push(move)
		score = evaluate_board(board)
		if score > bestscore:
			bestscore = score
			bestmove = move
		board.pop()

	board.push(bestmove)
	return str(bestmove)

print(board)

def evaluate_board(board):
	score = 0
	pieces = board.piece_map()

	for piece in pieces.values():
		score += PIECE_VALUES[piece.symbol()]
		
	return score

#######TEMPORARY SECTION - USER INPUT SO WE CAN INTERACT WITH THE ENGINE, WILL 
#######DISABLE WHEN WE NEED TO CONVERT TO UCI#################
end = False

def input_move(board):
	move = input("Input move (UCI 4 char str ONLY):\n")
	move = chess.Move.from_uci(move)
	board.push(move)
	print(board)
	print()

def input_uci():
	global board
	message = input("")
	with open("log.txt", "a") as log:
	    log.write(message + '\n')
	tokens = message.split()
	if tokens[0] == 'uci':
		print("id name EngineTest")
		print("id author DTD")
		print('uciok')
	elif tokens[0] == 'ucinewgame':
		board = chess.Board()
	elif tokens[0] == 'position' and len(tokens) == 2 and tokens[1] == 'startpos':
		board = chess.Board()
	elif tokens[0] == 'position' and len(tokens) > 3 and tokens[1] == 'startpos' and tokens[2] == 'moves':
		moves = tokens[3:]
		board = chess.Board()
		for move in moves:
			board.push(board.parse_uci(move))
		print(board)
	elif tokens[0] == 'position' and len(tokens) > 2 and tokens[1] == 'fen':
		board = chess.Board(fen=" ".join(tokens[2:]))
	elif tokens[0] == 'go':
		print('bestmove ' + AI_move(board))
	elif tokens[0] == 'stop':
		print(AI_move(board))
	elif tokens[0] == 'isready':
		print('readyok')
	elif tokens[0] == 'setoption':
		# TODO: We might need to implement some options
		pass
	elif tokens[0] == 'deb':
		print(board)
	elif tokens[0] == 'test':
		print(board.piece_map())	
	elif tokens[0] == 'quit':
		quit()
	else: 
		print("Unrecognized Command")

def temp_game_loop(end, board):
	
	while not end:
		if board.turn:
			input_uci()
		else:
			AI_move(board)

if __name__ == "__main__":
	temp_game_loop(False, board)