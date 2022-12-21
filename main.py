#!/usr/bin/env python3

import ai
import chess
import sys

def inputMove(board):
	move = input()
	
	# Assume judge will handle all invalid cases
	board.push(chess.Move.from_uci(move))

def aiMove(board):
	bestMove = ai.getBestMove(board)
	board.push(bestMove)
	print(bestMove)

def main(argv):
	player = -1
	
	if (argv[1] == "white"):
		player = chess.WHITE
	else:
		player = chess.BLACK
	
	board = chess.Board()

	while (True):
		if (board.turn == player):
			aiMove(board)
		else:
			inputMove(board)
		
		if board.is_game_over():
			print(board.outcome().result())
			break

#		print(board)
#		print()
			
main(sys.argv)