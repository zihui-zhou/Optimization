#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gurobipy import *

try:

    # Create a new model
    m = Model("HW1")

    # Create variables (lowerbound of 0 by default)
    x1 = m.addVar(vtype=GRB.CONTINUOUS, name="x1", lb=0)
    x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2", lb=0)
    x3 = m.addVar(vtype=GRB.CONTINUOUS, name="x3", lb=0)
    x4 = m.addVar(vtype=GRB.CONTINUOUS, name="x4", lb=0)


    # Integrate new variables
    m.update()

    # Set objective
    # m.setObjective
    m.setObjective(60*x1 + 40*x2 + 130*x3 + 90*x4 - 40*(x1 + x2 + x3 + x4), GRB.MAXIMIZE)

    # Add constraint: 
    m.addConstr(x1 + x3 == x2 + x4, "c1")
    m.addConstr(x1 + x2 + x3 + x4 <= 20, "c2")
    m.addConstr(x3 + 0.75*x4 <= 8, "c3")

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

except GurobiError:
    print 'Error reported'


# In[ ]:




