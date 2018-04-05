import chess
import math

"""
TODO:

- Implement more UCI features
  - Iterative Deepening, to allow a customizable thinking time

- Make it harder, better, faster, & stronger

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
SEARCH_DEPTH = 4

# Choose a move
def AI_move(board):
	move = search(board)
	board.push(move)
	return str(move)

def search(board):
	bestscore = -999999
	bestmove = None

	for move in board.legal_moves: 
		board.push(move)
		score = minimax(SEARCH_DEPTH, board, False, -1000000, 1000000)
		print(score)
		if score > bestscore:
			bestscore = score
			bestmove = move
		board.pop()

	return bestmove


def minimax(depth, board, isWhite, alpha, beta):
	if depth == 0:
		return evaluate_board(board)
	bestmove = None
	if not isWhite:
		bestscore = -999999
		for move in board.legal_moves: 
			board.push(move)
			score = minimax(depth - 1, board, not isWhite, alpha, beta)
			bestscore = max(bestscore, score)
			board.pop()
			alpha = max(alpha, bestscore)
			if beta <= alpha:
				return bestscore
		return bestscore
	else: 
		bestscore = 999999
		for move in board.legal_moves: 
			board.push(move)
			score = minimax(depth - 1, board, not isWhite, alpha, beta)
			bestscore = min(bestscore, score)
			board.pop()
			beta = min(beta, bestscore)
			if beta <= alpha:
				return bestscore
		return bestscore

def evaluate_board(board):
	score = 0
	pieces = board.piece_map()

	for piece in pieces.values():
		score += PIECE_VALUES[piece.symbol()]

	return score


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
	elif tokens[0] == 'position' and len(tokens) > 3 \
	and tokens[1] == 'startpos' and tokens[2] == 'moves':
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

print(board)
while True:
	input_uci()