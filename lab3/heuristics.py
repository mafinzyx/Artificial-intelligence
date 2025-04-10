from connect4 import Connect4

"""
    Functions here should return a scalar value of a current 'position'
    in Connect4 game as seen for player playing with 'token' (one of ['o', 'x']).
"""

def simple_score(position: Connect4, token="x"):
    score = 0
    
    if position.wins == token:
        return 10000
    elif position.wins == ( 'o' if token == 'x' else 'x'):
        return -10000
    elif position.wins is None:
        return 0

    for four in position.iter_fours():
        my_count = four.count(token)
        opponent_count = four.count('o' if token == 'x' else 'x')
        empty_count = four.count('_')

        if my_count == 3 and empty_count == 1:
            score += 10
        if opponent_count == 3 and empty_count == 1:
            score -= 10

    return score


def advanced_score(position: Connect4, token="x"):
    score = 0
    
    if position.wins == token:
        return 10000
    elif position.wins == ( 'o' if token == 'x' else 'x'):
        return -10000
    elif position.wins is None:
        return 0

    for four in position.iter_fours():
        my_count = four.count(token)
        opponent_count = four.count('o' if token == 'x' else 'x')
        empty_count = four.count('_')

        if my_count == 3 and empty_count == 1:
            score += 15
        if opponent_count == 3 and empty_count == 1:
            score -= 15

    center_column = position.center_column()
    center_token_count = center_column.count(token)
    opponent_center_token_count = center_column.count('o' if token == 'x' else 'x')

    score += 2 * (center_token_count - opponent_center_token_count)
    
    return score
