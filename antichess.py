#!/usr/bin/env python3

import chess

def legal_moves(board) -> list:
	moves = []
	for move in list(board.legal_moves):
		if (board.is_capture(move)):
			moves.append(move)
	
	return moves if moves else list(board.legal_moves)
	
# Counts the number of remaining pieces on the board
def remainingPieces(board):
	c = 0
	for sq in chess.SQUARES:
		if board.piece_at(sq):
			c += 1
			
	return c
