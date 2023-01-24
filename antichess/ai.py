#!/usr/bin/env python3

import antichess
import chess
import math
import random

from config import *

# White always maximize, Black always minimize
def payoff(board):
	mgScore = 0
	egScore = 0
	gamePhase = 0

	for sq in chess.SQUARES:
		piece = board.piece_at(sq)
		if not piece:
			continue

		pos = -1
		if piece.color == chess.WHITE:
			pos = (7 - int(sq / 8)) * 8 + sq % 8
			mgScore += (mg_pc_val[piece.piece_type - 1] + mg_pos_val[piece.piece_type - 1][pos])
			egScore += (eg_pc_val[piece.piece_type - 1] + eg_pos_val[piece.piece_type - 1][pos])

		else:
			pos = int(sq / 8) * 8 + (7 - sq % 8)
			mgScore -= (mg_pc_val[piece.piece_type - 1] + mg_pos_val[piece.piece_type - 1][pos])
			egScore -= (eg_pc_val[piece.piece_type - 1] + eg_pos_val[piece.piece_type - 1][pos])

		gamePhase += gamePhaseInc[piece.piece_type - 1]

	# Handles game board that is game over but the king is not captured
	if board.is_game_over():
		if board.outcome().winner == chess.WHITE:
			mgScore += mg_pc_val[5]
			egScore += eg_pc_val[5]
		elif board.outcome().winner == chess.BLACK:
			mgScore -= mg_pc_val[5]
			egScore -= eg_pc_val[5]

	mgPhase = min(egThreshold, gamePhase)
	egPhase = egThreshold - mgPhase
	score = (mgScore * mgPhase + egScore * egPhase) / egThreshold
	
	return score

# White is always the maximizing player
# And Black is always the minimizing player
def minimax(board, depth, alpha, beta, player):
	if depth == 0 or board.is_game_over():
		return payoff(board), board.copy()
	
	if player == chess.WHITE:
		maxScore = -math.inf
		maxBoard = board.copy()
		
		moves = antichess.legal_moves(board)
		random.shuffle(moves)

		for move in moves:
			board.push(move)

			# Since it is often in antichess that moves were limited due to captures,
			# we do not decrease the depth to allow more searches.
			if len(moves) <= 2:
				rScore, rBoard = minimax(board, depth, alpha, beta, chess.BLACK)
			else:
				rScore, rBoard = minimax(board, depth - 1, alpha, beta, chess.BLACK)

			if rScore > maxScore:
				maxScore = rScore
				maxBoard = rBoard

			board.pop()

			alpha = max(alpha, rScore)
			if beta <= alpha:
				break
			
		return maxScore, maxBoard

	else:
		minScore = math.inf
		minBoard = board.copy()
		
		moves = antichess.legal_moves(board)
		for move in moves:
			board.push(move)

			# Since it is often in antichess that moves were limited due to captures,
			# we do not decrease the depth to allow more searches.
			if len(moves) <= 2:
				rScore, rBoard = minimax(board, depth, alpha, beta, chess.WHITE)
			else:
				rScore, rBoard = minimax(board, depth - 1, alpha, beta, chess.WHITE)

			if rScore < minScore:
				minScore = rScore
				minBoard = rBoard

			board.pop()

			beta = min(beta, rScore)
			if beta <= alpha:
				break
			
		return minScore, minBoard

def validate(board, move):
	return move in antichess.legal_moves(board)

def getBestMove(board, depth):
	moves = antichess.legal_moves(board)

	# Safe computation time if only one move is feasible
	if len(moves) == 1:
		return moves[0]

	player = board.turn
	rScore, rBoard = minimax(board, depth, -math.inf, math.inf, player)

	bestMove = moves[0]
	try:
		bestMove = rBoard.move_stack[len(board.move_stack)]

		if not validate(board, bestMove):
			raise Exception(f"Move ${bestMove} is invalid")

	except:
		# Perform a random move on error
		bestMove = moves[0]
	return bestMove