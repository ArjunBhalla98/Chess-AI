import chess
import math
from evaluate import *
import pickle
import random
"""
TODO:

- Implement more UCI features
    - Iterative Deepening, to allow a customizable thinking time

- Make it harder, better, faster, & stronger

"""

# Setup Main Board
board = chess.Board()
SEARCH_DEPTH = 4
EPSILON_VALUE = 0.05
REWARDS = {"1-0": 1, "0-1": -1, "1/2-1/2": 0}
LEARNING_RATE = 0.75

board_minimax_scores = {}
board_minimax_scores_black = {}




# Choose a move
def AI_move(board):
    bestscore = -99999999999999999
    bestmove = None
    moves = []

    for move in board.legal_moves:
        board.push(move)
        score = minimax(SEARCH_DEPTH - 1, board, True, -1000000, 1000000)
        moves.append((move, score))
        if score > bestscore:
            bestscore = score
            bestmove = move
        board.pop()


    rand_prob = random.random()
    if rand_prob <= EPSILON_VALUE:
    	best = random.choice(moves)
    	bestscore = best[1]
    	bestmove = best[0]

    b_fen = board.board_fen()
    if board.turn == chess.WHITE:
        board_minimax_scores[b_fen] = bestscore
    else:
        board_minimax_scores_black[b_fen] = bestscore


    board.push(bestmove)

    if board.is_game_over():
        print("YEETH")
        update_weights(board)

    print(board)
    return str(bestmove)


def minimax(depth, board, isWhite, alpha, beta):
    if depth == 0:
        # print("info currmove "
            #   + " ".join(str(mov) for mov in board.move_stack))
        if isWhite:
            return -1*evaluate_board(board)
        else:
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
            print("WE ARE THE CHAMPIONS")
            quit()
        else:
            print("Unrecognized Command")


print(board)


def update_weights(board):

    with open("position_weights.pickle", "rb") as handle:
        weights_dict = pickle.load(handle)

    result = board.result()
    reward_winner = REWARDS[result]
    reward_loser = -1*reward_winner
    print(result)
    
    alpha = LEARNING_RATE*reward_winner
    alpha_opposite = LEARNING_RATE*reward_loser - 0.15 # Don't you worry your little head about that number bud

    if result == '1-0': # WHITE WON
        for board_fen in board_minimax_scores:
            print(board_fen)
            brd = board.set_fen(board_fen)
            for square, piece in brd.piece_map().items():
                symbol = piece.symbol()
                weights_dict[symbol][chess.square_rank(square)][chess.square_file(square)] += alpha

        for board_fen in board_minimax_scores_black:
            brd = board.set_fen(board_fen)
            for square, piece in brd.piece_map().items():
                symbol = piece.symbol()
                weights_dict[symbol][chess.square_rank(square)][chess.square_file(square)] += alpha_opposite

    elif result == '0-1':

        for board_fen in board_minimax_scores_black:
            print(board_fen)
            brd = board.set_fen(board_fen)
            for square, piece in brd.piece_map().items():
                symbol = piece.symbol()
                weights_dict[symbol][chess.square_rank(square)][chess.square_file(square)] += alpha

        for board_fen in board_minimax_scores:
            brd = board.set_fen(board_fen)
            for square, piece in brd.piece_map().items():
                symbol = piece.symbol()
                weights_dict[symbol][chess.square_rank(square)][chess.square_file(square)] += alpha_opposite

    with open("positions_weights.pickle", "wb") as handle:
        pickle.dump(weights_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)



######################################## Monte Carlo Reinforcement Learning METHODS ####################################################

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
