#!/usr/bin/python
import sys
import math

from log import Logger

class node:
  def __init__(self, nodeID):
    self.nodeID = nodeID
    self.outarc = []
    self.inarc = []
    self.b = 0

class arc:
  def __init__(self, arcID, tail, head, cost, cap):
    self.arcID = arcID
    self.tail = tail
    self.head = head
    self.cost = cost
    self.cap = cap

  def printit(self):
    print("arc ", self.arcID, "(", self.tail,", ", self.head,") cost =", self.cost)
    print("cap =",self.cap)

def datareader(log, dataname):
  log.jointoutput("reading network file " + dataname + "\n")
  n = 0
  m = 0
  try:
    f = open(dataname,"r")
    lines = f.readlines()
    f.close()
  except IOError as e:
    log.jointoutput("cannot open data file " + dataname + "\n")
    log.stateandquit("failure")

  thisline = lines[0].split()
  if len(thisline) != 4:
    log.stateandquit("illegal file structure; first line MUST be of the form n xxx m yyy\n")
  n = int(thisline[1])
  m = int(thisline[3])

  log.jointoutput("m = " + str(n) + " m = " + str(m) + "\n")
  if n <= 0 or m <= 0:
    log.stateandquit("illegal inputs")


  linenum = 0

  lookingforNETWORK = 1
  while lookingforNETWORK and linenum < len(lines)-1:
    linenum += 1
    thisline = lines[linenum].split()
    if len(thisline) > 0:
      if thisline[0] == "NETWORK":
        lookingforNETWORK = 0
  if lookingforNETWORK:
    log.stateandquit("NETWORK not found\n")
  nodes = []
  nodecount = 0
  while nodecount < n:
    thisnode = node(nodecount + 1)
    nodes.append(thisnode)
    nodecount += 1

  arcs = []
  arccount = 0
  while arccount < m:
    linenum += 1
    thisline = lines[linenum].split()
    if len(thisline) > 0:
      if len(thisline) != 4:
        log.jointoutput("error on line " + str(linenum + 1) + "\n")
        log.stateandquit("format must be i j cost cap\n")
      i = int(thisline[0])
      j = int(thisline[1])
      if i <= 0 or i > n or j <= 0 or j > n:
        log.jointoutput("illegal arc on line " + str(linenum + 1) + "\n")
        log.stateandquit("arc has ends: "  + str(i) + " " + str(j) + "\n")
      cost = float(thisline[2])
      cap = float(thisline[3])
      if cap < 0:
        log.jointoutput("illegal arc on line " + str(linenum + 1) + "\n")
        log.stateandquit("cap is "  + str(cap) + "\n")
      thisarc = arc(arccount + 1, i, j, cost, cap)
      arcs.append(thisarc)
      arccount += 1

  lookingforNETSUPPLIES = 1
  while lookingforNETSUPPLIES and linenum < len(lines)-1:
    linenum += 1
    thisline = lines[linenum].split()
    if len(thisline) > 0:
      if thisline[0] == "NETSUPPLIES":
        lookingforNETSUPPLIES = 0
  if lookingforNETSUPPLIES:
    log.stateandquit("NETSUPPLIES not found\n")

  sumb = 0
  lookingforEND = 1
  while lookingforEND and linenum < len(lines)-1:
    linenum += 1
    thisline = lines[linenum].split()
    if len(thisline) > 0:
      if thisline[0] == "END":
        log.jointoutput("found END on line " + str(linenum + 1) + "\n")
        lookingforEND = 0
      else:
        if len(thisline) != 2:
          log.jointoutput("error on line " + str(linenum + 1) + "\n")
          log.stateandquit("format must be i b[i]\n")
        i = int(thisline[0])
        if i <= 0 or i > n:
          log.jointoutput("illegal rhs line " + str(linenum + 1) + "\n")
          log.stateandquit("node is: "  + str(i) + "\n")
        rhs = float(thisline[1])
        nodes[i-1].b = rhs
        sumb += rhs

  if math.fabs(sumb) > 0.00000001:
    log.stateandquit("illegal sum of b's: "  + str(sumb) + "\n")
  if lookingforEND:
    log.stateandquit("END not found\n")


  log.jointoutput("Now constructing adjacencies\n")

  arcind = 0
  while arcind < m:
    i = arcs[arcind].tail
    j = arcs[arcind].head
    (nodes[i-1].outarc).append(arcind)
    (nodes[j-1].inarc).append(arcind)
    arcind += 1

  return n,m, nodes, arcs


def lpwriter(log, lpname, n, m, nodes, arcs):
  log.jointoutput("writing problem to  LP file " + lpname + "\n")
  try:
    f = open(lpname,"w")

  except IOError:
    log.jointoutput("cannot open lp file " + lpname + "\n")
    log.stateandquit("failure")

  f.write("Minimize\n")
  arcind = 0
  count = 0
  while arcind < m:
    i = arcs[arcind].tail
    j = arcs[arcind].head
    cost = arcs[arcind].cost
    if cost != 0:
      i = arcs[arcind].tail
      j = arcs[arcind].head

      if cost > 0:
        f.write(" +")
      f.write(" " + str(cost))
      f.write(" x_" + str(i)+ "," +str(j))
      count += 1
      if count >= 5:
        f.write("\n")
        count = 0

    arcind += 1
  if count > 0:
    f.write("\n")
  f.write("Subject To\n")
  i = 1
  while i <= n:
    f.write("balance_"+str(i)+": ")
    outdeg = len(nodes[i-1].outarc)
    indeg  = len(nodes[i-1].inarc)
    log.jointoutput("node " + str(i) + " has outdeg " + str(outdeg) + " indeg " + str(indeg) + "\n")
    k = 0
    count = 0
    while k < outdeg:
      j = arcs[nodes[i-1].outarc[k]].head
      f.write(" + x_" + str(i)+ "," +str(j))
      count += 1
      if count >= 5:
        f.write("\n")
        count = 0

      k += 1

    k = 0
    while k < indeg:
      j = arcs[nodes[i-1].inarc[k]].tail
      f.write(" - x_" + str(j)+ "," +str(i))
      count += 1
      if count >= 5:
        f.write("\n")
        count = 0

      k += 1

    f.write(" = " + str(nodes[i-1].b) + "\n")
#    j = 1
#    count = 0
#    doneit = 0
#    while j <= M:
#      cap = capacity[i*(M + 1) + j]
#      if cap > 0:
#        if doneit:
#          f.write(" + ")
#        doneit = 1
#        f.write(" x"+str(i)+","+str(j))
#        count += 1
#        if count >= 5:
#          f.write("\n")
#          count = 0
#      j += 1

    i += 1
#
#  j = 1
#  while j <= M:
#    f.write("Demand_"+str(j)+": ")
#    i = 1
#    count = 0
#    doneit = 0
#    while i <= N:
#      cap = capacity[i*(M + 1) + j]
#      if cap > 0:
#        if doneit:
#          f.write(" + ")
#        doneit = 1
#        f.write(" x"+str(i)+","+str(j))
#        count += 1
#        if count >= 5:
#          f.write("\n")
#        count = 0
#      i += 1
#    f.write(" = " + str(demand[j]) + "\n")
#    j += 1
#
#
  f.write("Bounds\n")
  arcind = 0
  while arcind < m:
    i = arcs[arcind].tail
    j = arcs[arcind].head

    f.write("x_" + str(i)+ "," +str(j)+ " <= " + str(arcs[arcind].cap) + "\n")
    arcind += 1


#  i = 1
#  while i <= N:
#    j = 1
#    while j <= M:
#      cap = capacity[i*(M + 1) + j]
#      if cap > 0:
############        f.write("x"+str(i)+","+str(j) + " <= " + str(capacity[i*(M + 1) + j]) + "\n")
#      j += 1
#    i += 1

  f.write("END\n")
  f.close()

################################
# main
###############################

if len(sys.argv) != 3:  # the program name, network file, lpfile
  # stop the program and print an error message
  sys.exit("usage: singlecomm.py network_file lpfile")

log = Logger("singlecomm.log")

log.jointoutput("network file: " + sys.argv[1] + "\n")

n,m,nodes,arcs = datareader(log, sys.argv[1])

lpwriter(log, sys.argv[2], n,m, nodes, arcs)


log.closelog()
