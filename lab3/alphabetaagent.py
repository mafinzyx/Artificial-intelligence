import math

from minmaxagent import MinMaxAgent

class AlphaBetaAgent(MinMaxAgent):
    def _minmax(self, game, depth, maximizing, alpha=-math.inf, beta=math.inf):
        if depth == 0 or game.game_over:
            return self._evaluate_board(game), None

        possible_moves = game.possible_drops()
        best_column = possible_moves[0]

        if maximizing:
            max_eval = -math.inf
            for col in possible_moves:
                simulated_game = self._simulate_move(game, col, self.my_token)
                eval_score, _ = self._minmax(simulated_game, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_column = col
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_column
        else:
            min_eval = math.inf
            for col in possible_moves:
                simulated_game = self._simulate_move(game, col, self.opponent_token)
                eval_score, _ = self._minmax(simulated_game, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_column = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_column
