### OR(1) MODELS AND APPLICATIONS - COURSERA ASSIGNMENT - WEEK 6 - Q2 ###
# LINEAR PROGRAMMING

import math
import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB

############################################### SETS AND INDICES ###############################################

num_points = 15
P = [f'Point{p+1}' for p in range(num_points)]

############################################### PARAMETERS ###############################################

x = [38, 56, 50, 52, 37, 60, 67, 54, 59, 43, 30, 53, 59, 40, 65]
y = [137, 201, 152, 107, 150, 173, 194, 166, 154, 137, 38, 193, 154, 175, 247]

############################################### FORMULATION ###############################################

model = gp.Model("curve_fitting")

############################################### DECISION VARIABLES ###############################################

a = model.addVar(-math.inf, math.inf, name="a")
b = model.addVar(-math.inf, math.inf, name="b")

Y = {}
for n in range(num_points):
    Y[n] = model.addVar(-math.inf, math.inf, name=f"Y_{n}")

D = {}
for n in range(num_points):
    D[n] = model.addVar(0, math.inf, name=f"D_{n}")

################################################################### CONSTRAINTS ###################################################################

# expected values of y in the linear equation
for n in range(num_points):
    model.addConstr(Y[n] == b*x[n] + a)

# deviations of y
for n in range(num_points):
    model.addConstr(D[n] >= Y[n] - y[n])
    model.addConstr(D[n] >= y[n] - Y[n])

################################################################### OBJECTIVE ###################################################################

objective_function = gp.quicksum(D[n]*D[n] for n in range(num_points))
model.setObjective(objective_function, GRB.MINIMIZE)

################################################################### SOLVER ###################################################################

model.optimize()

################################################################### OUTPUT ###################################################################

if model.status == GRB.OPTIMAL:
    print('Total absolute deviation -', model.objVal, '\n')
    print('best straight line - y =', b.x, '*x +', a.x, '\n')

else:
    print('The problem does not have an optimal solution.')