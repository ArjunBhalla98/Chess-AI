import evaluate
import chess

def q_function(time, state, action):
	current_score = evaluate.evaluate_board()