#!/usr/bin/python3

### CSCI-B 351 / COGS-Q 351 Spring 2023


import math
from board import Board
from pip._vendor import requests

class BasePlayer:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    ##################
    #      TODO      #
    ##################
    # Assign integer scores to the three terminal states
    # P2_WIN_SCORE < TIE_SCORE < P1_WIN_SCORE
    # Access these with "self.TIE_SCORE", etc.
        self.P1_WIN_SCORE = 100
        self.P2_WIN_SCORE = -100
        self.TIE_SCORE =  0

    # Returns a heuristic for the board position
    # Good positions for 0 pieces should be positive and
    # good positions for 1 pieces should be negative
    # for all boards, P2_WIN_SCORE < heuristic(b) < P1_WIN_SCORE
    def heuristic(self, board):
        p1_stones = 0
        p2_stones = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    p1_stones += 1
                elif board[i][j] == 1:
                    p2_stones += 1
        stone_difference = p1_stones - p2_stones
        if stone_difference > 0:
            return (stone_difference / (p1_stones + p2_stones) * self.P1_WIN_SCORE)
        elif stone_difference < 0:
            return (stone_difference / (p1_stones + p2_stones) * self.P2_WIN_SCORE)
        else:
            return self.TIE_SCORE


    def findMove(self, trace):
        raise NotImplementedError

class ManualPlayer(BasePlayer):
    def __init__(self, max_depth=None):
        BasePlayer.__init__(self, max_depth)

    def findMove(self, trace):
        board = Board(trace)
        opts = "  "
        for c in range(6):
            opts += " "+(str(c+1) if board.isValidMove(c) else ' ')+"  "

        while True:
            if(board.turn == 0):
                print("\n")
                board.printSpaced()
                print(opts)
                pit = input("Pick a pit (P1 side): ")
            else:
                print("\n")
                print(" " + opts[::-1])
                board.printSpaced()
                pit = input("Pick a pit (P2 side): ")
            try: pit = int(pit) - 1
            except ValueError: continue
            if board.isValidMove(pit):
                return pit

class RandomPlayer(BasePlayer):
    def __init__(self, max_depth=None):
        BasePlayer.__init__(self, max_depth)
        self.random = random.Random(13487951347859)
    def findMove(self, trace):
        board = Board(trace)
        options = list(board.getAllValidMoves())
        return self.random.choice(options)

class RemotePlayer(BasePlayer):
    def __init__(self, max_depth=None):
        BasePlayer.__init__(self, max_depth)
        self.instructor_url = "http://silo.cs.indiana.edu:30005"
        if self.max_depth > 8:
            print("It refused to go that hard. Sorry.")
            self.max_depth = 8
    def findMove(self, trace):
        r = requests.get(f'{self.instructor_url}/getmove/{self.max_depth},{trace}')
        move = int(r.text)
        return move


class PlayerMM(BasePlayer):
    ##################
    #      TODO      #
    ##################
    # performs minimax on board with depth.
    # returns the best move and best score as a tuple
    def minimax(self, board, depth):
        if board.winner() or depth == 0:
            if board.winner() == -1:
                return None, self.TIE_SCORE
            elif board.winner() == 0:
                return None, self.P1_WIN_SCORE
            else:
                return None, self.P2_WIN_SCORE
        best_move = None
        best_score = float('-inf') if board.turn == 1 else float('inf')
        for move in board.getAllValidMoves():
            new_board = board.makeMove(move)
            _, score = self.minimax(new_board, depth - 1)
            if board.turn == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move, best_score

    def findMove(self, trace):
        board = Board(trace)
        move, score = self.minimax(board, self.max_depth)
        return move

class PlayerAB(BasePlayer):
    ##################
    #      TODO      #
    ##################
    # performs minimax with alpha-beta pruning on board with depth.
    # alpha represents the score of max's current strategy
    # beta  represents the score of min's current strategy
    # in a cutoff situation, return the score that resulted in the cutoff
    # returns the best move and best score as a tuple
    def alphaBeta(self, board, depth, alpha, beta):
        if board.winner() or depth == 0:
            if board.winner() == -1:
                return None, self.TIE_SCORE
            elif board.winner() == 0:
                return None, self.P1_WIN_SCORE
            else:
                return None, self.P2_WIN_SCORE
        best_move = None
        best_score = float('-inf') if board.turn == 1 else float('inf')
        for move in board.getAllValidMoves():
            new_board = board.makeMove(move)
            _, score = self.alphaBeta(new_board, depth - 1, alpha, beta)
            if board.turn == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
            if beta <= alpha:
                break
                
            return best_move, best_score

    def findMove(self, trace):
        board = Board(trace)
        move, score = self.alphaBeta(board, self.max_depth, -math.inf, math.inf)
        return move

class PlayerDP(PlayerAB):
    ''' A version of PlayerAB that implements dynamic programming
        to cache values for its heuristic function, improving performance. '''
    def __init__(self, max_depth):
        PlayerAB.__init__(self, max_depth)
        self.resolved = {}

    ##################
    #      TODO      #
    ##################
    # if a saved heuristic value exists in self.resolved for board.state, returns that value
    # otherwise, uses BasePlayer.heuristic to get a heuristic value and saves it under board.state
    def heuristic(self, board):
        raise NotImplementedError


class PlayerBonus(BasePlayer):
    ''' This class is here to give you space to experiment for your ultimate Mancala AI,
        your one and only PlayerBonus. This is only used for the extra credit tournament. '''
    def findMove(self, trace):
        raise NotImplementedError

#######################################################
###########Example Subclass for Testing
#######################################################

# This will inherit your findMove from above, but will override the heuristic function with
# a new one; you can swap out the type of player by changing X in "class TestPlayer(X):"
class TestPlayer(BasePlayer):
    # define your new heuristic here
    def heuristic(self):
        pass


