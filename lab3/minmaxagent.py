import math
from exceptions import GameplayException
from connect4 import Connect4

class MinMaxAgent:
    def __init__(self, token, depth=4):
        self.my_token = token
        self.opponent_token = 'o' if token == 'x' else 'x'
        self.depth = depth

    def decide(self, game: Connect4):
        _, column = self._minmax(game, self.depth, True)
        return column

    def _minmax(self, game, depth, maximizing):
        if depth == 0 or game.game_over:
            return self._evaluate_board(game), None

        possible_moves = game.possible_drops()
        best_column = possible_moves[0]
        
        if maximizing:
            max_eval = -math.inf
            for col in possible_moves:
                simulated_game = self._simulate_move(game, col, self.my_token)
                eval_score, _ = self._minmax(simulated_game, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_column = col
            return max_eval, best_column
        else:
            min_eval = math.inf
            for col in possible_moves:
                simulated_game = self._simulate_move(game, col, self.opponent_token)
                eval_score, _ = self._minmax(simulated_game, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_column = col
            return min_eval, best_column

    def _simulate_move(self, game, column, token):
        simulated_game = Connect4(game.width, game.height)
        simulated_game.board = [row[:] for row in game.board]
        simulated_game.who_moves = game.who_moves
        simulated_game.game_over = game.game_over
        simulated_game.wins = game.wins

        simulated_game.drop_token(column)
        return simulated_game

    def _evaluate_board(self, game):
        if game.wins == self.my_token:
            return 1000
        elif game.wins == self.opponent_token:
            return -1000

        score = 0
        for four in game.iter_fours():
            score += self._evaluate_four(four)
            
        return score

    def _evaluate_four(self, four):
        score = 0
        my_count = four.count(self.my_token)
        opponent_count = four.count(self.opponent_token)
        empty_count = four.count('_')

        if my_count == 4:
            score += 100
        elif my_count == 3 and empty_count == 1:
            score += 10
        elif my_count == 2 and empty_count == 2:
            score += 5

        if opponent_count == 4:
            score -= 100
        elif opponent_count == 3 and empty_count == 1:
            score -= 10
        elif opponent_count == 2 and empty_count == 2:
            score -= 5

        return score
    
    
