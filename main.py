#!/usr/bin/env python3

import ai
import chess
import config
import sys
import time

def inputMove(board):
	move = input()
	
	# Assume judge will handle all invalid cases
	board.push(chess.Move.from_uci(move))

def aiMove(board, timeElapsed):
	# Reduce search depth as time limit approaches
	if timeElapsed >= config.warnTime2:
		bestMove = ai.getBestMove(board, config.orgDepth - 2)
	elif timeElapsed >= config.warnTime1:
		bestMove = ai.getBestMove(board, config.orgDepth - 1)
	else:
		bestMove = ai.getBestMove(board, config.orgDepth)

	board.push(bestMove)
	print(bestMove)

def main(argv):
	player = -1
	
	if (argv[1] == "white"):
		player = chess.WHITE
	else:
		player = chess.BLACK
	
	board = chess.Board()
	timeElapsed = 0

	while (True):
		if (board.turn == player):
			startTime = time.time()
			aiMove(board, timeElapsed)
			endTime = time.time()
			timeElapsed += (endTime - startTime)
			
		else:
			inputMove(board)
		
		if board.is_game_over():
			print(board.outcome().result())
			break
			
main(sys.argv)