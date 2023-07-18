### OR(1) MODELS AND APPLICATIONS - COURSERA ASSIGNMENT - WEEK 6 - Q1 ###
# LINEAR PROGRAMMING

import math
import numpy as np
import pandas as pd

from ortools.linear_solver import pywraplp

############################################### SETS AND INDICES ###############################################

num_products = 7
num_materials = 3

P = [f'Product {p+1}' for p in range(num_products)]
M = [f'Material {m+1}' for m in range(num_materials)]

################################################################### PARAMETERS ###################################################################

material = [[0,3,10], 
            [5,10,10],
            [5,3,9],
            [4,6,3],
            [8,2,8],
            [5,2,10],
            [3,2,7]]

price = [100,120,135,90,125,110,105]

supply = [100,150,200]

################################################################### FORMULATION ###################################################################

solver = pywraplp.Solver.CreateSolver('SCIP')

################################################################### DECISION VARIABLES ################################################################### 

Prod = {} # Amount of product p
for p in range(num_products):
    Prod[p] = solver.NumVar(0, math.inf, 'Prod[p]')

################################################################### CONSTRAINTS ###################################################################

for m in range(num_materials):
    solver.Add(solver.Sum([material[p][m]*Prod[p] for p in range(num_products)]) <= supply[m])

################################################################### OBJECTIVE ###################################################################

objective_function = []

for p in range(num_products):
    objective_function.append(price[p]*Prod[p])

################################################################### SOLVER ###################################################################

solver.Maximize(solver.Sum(objective_function))
status = solver.Solve()

################################################################### OUTPUT ###################################################################

if status == pywraplp.Solver.OPTIMAL:
    obj = round(solver.Objective().Value(),2)
    print('\nProfit =',obj,'\n')    
    P_value = [round(Prod[p].solution_value(),2) for p in range(num_products)]
    print(pd.DataFrame(P_value, index = P, columns = ['Quantity']),'\n')

else:
    print('The problem does not have an optimal solution.')