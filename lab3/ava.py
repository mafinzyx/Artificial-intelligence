import time

from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from alphabetaagent import AlphaBetaAgent

GAMES_COUNT = 3
game_number = 0
agent1_wins = 0
agent2_wins = 0

print("AlphaBeta Algorytm testing: \n")
for i in range(GAMES_COUNT):
    connect4 = Connect4(width=8, height=7)
    agent1 = RandomAgent('o')
    agent2 = AlphaBetaAgent('x')
    
    game_number += 1
    print("\nGame number: ", game_number)

    start_time = time.time()

    while not connect4.game_over:
        #connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')

    end_time = time.time()
    game_duration = end_time - start_time
    
    connect4.draw()

    if connect4.wins == agent1.my_token:
        agent1_wins += 1
    elif connect4.wins == agent2.my_token:
        agent2_wins += 1

    print("Agent1(O) wins count: ", agent1_wins)
    print("Agent2(X) wins count: ", agent2_wins)
    print(f"Game duration: {game_duration:.2f} seconds")

print("MinMax heurystyczny testing: \n")
game_number = 0
for i in range(GAMES_COUNT):
    connect4 = Connect4(width=8, height=7)
    agent1 = RandomAgent('o')
    agent2 = MinMaxAgent('x')
    
    game_number += 1

    print("\nGame number: ", game_number)

    start_time = time.time()

    while not connect4.game_over:
        #connect4.draw()
        try:
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(connect4)
            else:
                n_column = agent2.decide(connect4)
            connect4.drop_token(n_column)
        except (ValueError, GameplayException):
            print('invalid move')

    end_time = time.time()
    game_duration = end_time - start_time
    
    connect4.draw()

    if connect4.wins == agent1.my_token:
        agent1_wins += 1
    elif connect4.wins == agent2.my_token:
        agent2_wins += 1

    print("Agent1(O) wins count: ", agent1_wins)
    print("Agent2(X) wins count: ", agent2_wins)
    print(f"Game duration: {game_duration:.2f} seconds")