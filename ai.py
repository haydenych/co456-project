#!/usr/bin/env python3

import antichess
import chess
import math
import time

from config import *

def payoff(board):
	score = 0
	for sq in chess.SQUARES:
		piece = board.piece_at(sq)
		if not piece:
			continue
		
		pos = -1
		if piece.color == chess.WHITE:
			pos = (7 - int(sq / 8)) * 8 + sq % 8
			
			if piece.piece_type == chess.PAWN:
				score += (P + pawn[pos])
			elif piece.piece_type == chess.KNIGHT:
				score += (N + knight[pos])
			elif piece.piece_type == chess.BISHOP:
				score += (B + bishop[pos])
			elif piece.piece_type == chess.ROOK:
				score += (R + rook[pos])
			elif piece.piece_type == chess.QUEEN:
				score += (Q + queen[pos])
			elif piece.piece_type == chess.KING and antichess.remainingPieces(board) > 12:
				score += (K + king_mid[pos])
			else:
				score += (K + king_end[pos])
				
		else:
			pos = int(sq / 8) * 8 + (7 - sq % 8)
		
			if piece.piece_type == chess.PAWN:
				score -= (P + pawn[pos])
			elif piece.piece_type == chess.KNIGHT:
				score -= (N + knight[pos])
			elif piece.piece_type == chess.BISHOP:
				score -= (B + bishop[pos])
			elif piece.piece_type == chess.ROOK:
				score -= (R + rook[pos])
			elif piece.piece_type == chess.QUEEN:
				score -= (Q + queen[pos])
			elif piece.piece_type == chess.KING and antichess.remainingPieces(board) > 12:
				score -= (K + king_mid[pos])
			else:
				score -= (K + king_end[pos])

	# Handles game board that is game over but the king is not captured
	if board.is_game_over():
		if board.outcome().winner == chess.WHITE:
			score += K
		elif board.outcome().winner == chess.BLACK:
			score -= K

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
	player = board.turn
	maxScore, maxBoard = minimax(board, depth, -math.inf, math.inf, player)

	bestMove = antichess.legal_moves(board)[0]
	
	try:
		# Handle first move
		if len(board.move_stack) == 0:
			bestMove = maxBoard.move_stack[0]
	
		else:
			for _ in range(depth):
				bestMove = maxBoard.pop()
				if board.peek() == maxBoard.peek():
					break
				
		if not validate(board, bestMove):
			raise Exception(f"Move ${bestMove} is invalid")

	except:
		# Perform a random move on error
		bestMove = antichess.legal_moves(board)[0]

	return bestMove