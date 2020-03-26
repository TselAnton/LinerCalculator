from pulp import *


# optimal_model == true -> max
# optimal_model == false -> min
def find_solution(num_of_const, optimal_model=True):
    x = [LpVariable("x" + str(i + 1), lowBound=0) for i in range(num_of_const)]
    problem = LpProblem("0", LpMaximize) if optimal_model else LpProblem("0", LpMinimize)

    print(x[0]*20+7*x[1]-x[2]*5)
    pass
