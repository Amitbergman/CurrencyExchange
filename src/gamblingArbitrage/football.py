
from scipy.optimize import linprog

def solveLinearProgrammingForArbitrage(win_1_rate, draw_rate, win_2_rate):
    # We will place 10 dollars on team 1
    # we would like to solve:
    # b  + c <= -10.1 + 10*win_1
    # b + (1-win_2)c <= -10
    # (1-draw)b + c <= -10
    c = [1, 1] #minimiza b + c
    A = [[1, 1], [1, 1-win_2_rate], [1-draw_rate, 1]]
    b = [-10.1+10*win_1_rate, -10.1, -10.1]
    res = linprog(c, A_ub=A, b_ub=b)
    return res

def CheckIfArbitrageExists(win_team_1_site_1, draw_site_1, win_team_2_site_1, win_team_1_site_2, draw_site_2, win_team_2_site_2):
    our_gainRate_if_team_1_wins = max(win_team_1_site_1, win_team_1_site_2)
    our_gainRate_if_draw = max(draw_site_1, draw_site_2)
    our_gainRate_if_team_2_wins = max(win_team_2_site_1, win_team_2_site_2)
    
    solution = solveLinearProgrammingForArbitrage(our_gainRate_if_team_1_wins, our_gainRate_if_draw, our_gainRate_if_team_2_wins)
    if (solution.success):
        print("Arbitrage exists")
        print("Bet on team 1: 10")
        print("Bet on draw: ", solution.x[0])
        print("Bet on team 2: ", solution.x[1])
    else:
        print("Try next time")

CheckIfArbitrageExists(1.35,3.8,5.8,1.6,3.7, 58)