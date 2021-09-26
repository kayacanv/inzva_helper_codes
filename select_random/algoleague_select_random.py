import pandas as pd
import random

leaderboard = pd.read_csv('/home/ekrem/Documents/inzva/inzva_helper_codes/select_random/leaderboard.csv')
print('Random Seed:',leaderboard['Penalty'].sum())
random.seed(leaderboard['Penalty'].sum())

print('random solver', leaderboard.iloc[random.randint(0, len(leaderboard) - 1)])

fully_solved = leaderboard[leaderboard['Solved'] >= 20]

print('random fully solver', fully_solved.iloc[random.randint(0, len(fully_solved) - 1)])