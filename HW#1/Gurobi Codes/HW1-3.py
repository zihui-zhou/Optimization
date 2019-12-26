#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gurobipy import *

try:
    # Create new model
    m = Model("HW1-3")
    
    # Create variables (lowerbound of 0 by default)
    x1 = m.addVar(vtype=GRB.CONTINUOUS, name="x1", lb=2)
    x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2", lb=0)
    x3 = m.addVar(vtype=GRB.CONTINUOUS, name="x3", lb=0)
    
    # Update the model
    m.update()
    
    # Set Objective
    m.setObjective(3*x1 - 2*x2, GRB.MINIMIZE)
    
    #Add constraints
    m.addConstr(3*x1 + x2 <= 12)
    m.addConstr(3*x1 - 2*x2 -x3 == 12)
    
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

