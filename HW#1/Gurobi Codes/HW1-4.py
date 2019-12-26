from gurobipy import *

# Create new model
m = Model("HW1-4")

# Create variables (lowerbound of 0 by default)
m1 = m.addVar(vtype=GRB.CONTINUOUS, name="m1", lb=0)
m2 = m.addVar(vtype=GRB.CONTINUOUS, name="m2", lb=0)
m3 = m.addVar(vtype=GRB.CONTINUOUS, name="m3", lb=0)
g6 = m.addVar(vtype=GRB.CONTINUOUS, name="g6", lb=0)
g8 = m.addVar(vtype=GRB.CONTINUOUS, name="g8", lb=0)
g10 = m.addVar(vtype=GRB.CONTINUOUS, name="g10", lb=0)
h6 = m.addVar(vtype=GRB.CONTINUOUS, name="h6", lb=0)
h8 = m.addVar(vtype=GRB.CONTINUOUS, name="h8", lb=0)
h10 = m.addVar(vtype=GRB.CONTINUOUS, name="h10", lb=0)
x6 = m.addVar(vtype=GRB.CONTINUOUS, name="x6", lb=0)
x8 = m.addVar(vtype=GRB.CONTINUOUS, name="x8", lb=0)

# Update the model
m.update()

# Set Objective
m.setObjective(12*(g6 + g8 + g10) + 5*(h6 + h8 + h10) - (3.4*m1 + 3*m2 + 2.6*m3 + x6 + 1.5*x8), GRB.MAXIMIZE)

#Add constraints
m.addConstr(g6 + h6 == 0.3*m1 + 0.4*m2 + 0.1*m3 - x6)
m.addConstr(g8 + h8 == 0.5*m1 + 0.2*m2 + 0.3*m3 - x8 + x6)
m.addConstr(g10 + h10 == 0.8*m1 + 0.4*m2 + 0.2*m3 + x8)
m.addConstr(g6 + g8 + g10 <= 2000)
m.addConstr(h6 + h8 + h10 <= 600)
m.addConstr((6*g6 + 8*g8 + 10*g10) >= 9) #/(g6 + g8 + g10)
m.addConstr((6*h6 + 8*h8 + 10*h10) >= 7) #/(h6 + h8 + h10)


# Optimize (model is updated when we optimize)
m.optimize()

#print model status (2 is optimal)
#https://www.gurobi.com/documentation/6.5/refman/optimization_status_codes.html
print 'Model status:', m.status

#print decision variables
for v in m.getVars():
    print v.varName, v.x

#print objective function value
print 'Obj:', m.objVal



