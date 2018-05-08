import chess
import math
from evaluate import *
import pickle
"""
TODO:

- Implement more UCI features
    - Iterative Deepening, to allow a customizable thinking time

- Make it harder, better, faster, & stronger

"""

# Setup Main Board
board = chess.Board()
SEARCH_DEPTH = 4


# Choose a move
def AI_move(board):
    bestscore = -999999
    bestmove = None

    for move in board.legal_moves:
        board.push(move)
        score = minimax(SEARCH_DEPTH - 1, board, True, -1000000, 1000000)
        if score > bestscore:
            bestscore = score
            bestmove = move
        board.pop()

    board.push(bestmove)
    print(board)
    return str(bestmove)


def minimax(depth, board, isWhite, alpha, beta):
    if depth == 0:
        # print("info currmove "
            #   + " ".join(str(mov) for mov in board.move_stack))
        return evaluate_board(board)
    bestmove = None
    if not isWhite:  # BLACK
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
    else:  # WHITE
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


def input_uci():
    global board

    message = input("")
    with open("log.txt", "a") as log:
        log.write(message + '\n')
    tokens = message.split()

    if len(tokens) > 0:
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

######################################## Monte Carlo Reinforcement Learning METHODS ####################################################
def init_dicts():
	with open("state_actions.pickle", "wb") as handle:
		pickle.dump({}, handle, protocol = pickle.HIGHEST_PROTOCOL)

def q_function(action, board):
	current_score = evaluate.evaluate_board(board)
	board.push(action)
	new_score = evaluate.evaluate_board(board)
	board.pop(action)
	reward = new_score - current_score

	with open("state_actions.pickle", "rb") as handle:
		sa_dict = pickle.load(handle)

	b_fen = board.board_fen()
	if b_fen not in sa_dict:
		sa_dict[b_fen] = {action:reward}
	else:
		if action not in sa_dict[b_fen]:
			sa_dict[b_fen][action] = reward
		else: # move already in dictionary
			sa_dict[b_fen][action] = (sa_dict[b_fen][action] + reward)/2

	with open("state_actions.pickle", "wb") as handle:
		pickle.dump(sa_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)

def pi_function(board):

	with open("state_actions.pickle", "rb") as handle:
		sa_dict = pickle.load(handle)

	b_fen = board.board_fen()

	if b_fen in sa_dict:
		max_reward = -9999
		for move in sa_dict[b_fen]:
			if sa_dict[b_fen][move] > max_reward:
				max_reward = sa_dict[b_fen][move]
	else:
		return None


while True:
    input_uci()
