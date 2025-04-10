import random, sys, math
from copy import deepcopy
from typing import Literal
from abc import ABC, abstractmethod
from exceptions import AgentException
from heuristics import simple_score, advanced_score
from connect4 import Connect4

class Agent(ABC):
    def __init__(self, my_token="o", **kwargs):
        self.my_token = my_token
        self.opponent_token = 'o' if my_token == 'x' else 'x'

    @abstractmethod
    def decide(self, connect4):
        pass

    def __str__(self):
        return f"{self.my_token} ({self.__class__.__name__})"

class RandomAgent(Agent):
    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException("not my round")
        return random.choice(connect4.possible_drops())

class MinMaxAgent(Agent):
    def __init__(self, my_token="o", depth=4, heuristic="simple"):
        super().__init__(my_token)
        self.depth = depth
        self.heuristic_fun = simple_score if heuristic == "simple" else advanced_score
    
    def decide(self, game: Connect4):
        if game.who_moves != self.my_token:
            raise AgentException("not my round")
        _, best_move = self._minmax(game, self.depth, True)
        return best_move

    def _minmax(self, game, depth, maximizing):
        if depth == 0 or game.game_over:
            return self.heuristic_fun(game, self.my_token), None
        
        possible_moves = game.possible_drops()
        best_move = possible_moves[0]

        if maximizing:
            max_eval = -math.inf
            for col in possible_moves:
                simulated_game = deepcopy(game)
                simulated_game.drop_token(col)
                eval_score, _ = self._minmax(simulated_game, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col
            return max_eval, best_move
        else:
            min_eval = math.inf
            for col in possible_moves:
                simulated_game = deepcopy(game)
                simulated_game.drop_token(col)
                eval_score, _ = self._minmax(simulated_game, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col
            return min_eval, best_move

class AlphaBetaAgent(MinMaxAgent):
    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException("not my round")
        _, best_move = self._alphabeta(connect4, self.depth, -sys.maxsize, sys.maxsize, True)
        return best_move

    def _alphabeta(self, game, depth, alpha, beta, maximizing):
        if depth == 0 or game.game_over:
            return self.heuristic_fun(game, self.my_token), None
        
        possible_moves = game.possible_drops()
        best_move = possible_moves[0]

        if maximizing:
            max_eval = -math.inf
            for col in possible_moves:
                simulated_game = deepcopy(game)
                simulated_game.drop_token(col)
                eval_score, _ = self._alphabeta(simulated_game, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for col in possible_moves:
                simulated_game = deepcopy(game)
                simulated_game.drop_token(col)
                eval_score, _ = self._alphabeta(simulated_game, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
