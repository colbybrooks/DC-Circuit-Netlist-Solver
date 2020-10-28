# Program solves DC circuits consisting of voltage and/or current source

import numpy as np                     # needed for arrays
from numpy.linalg import solve         # needed for matrices
from read_netlist import read_netlist  # supplied function to read the netlist
import comp_constants as COMP          # needed for the common constants
import pandas as pd

# this is the list structure that we'll use to hold components:
# [ Type, Name, i, j, Value ] ; set up an index for each component's property

############################################################
# How large a matrix is needed for netlist? This could     #
# have been calculated at the same time as the netlist was #
# read in but we'll do it here to handle special cases     #
############################################################

def ranknetlist(netlist):              # pass in the netlist

    list = [[e[2] for e in netlist], [e[3] for e in netlist]]   # Make a list of the i and j columns
    nodes = np.max(list)    # Sets nodes to the maximum number in the list ex. HW Problem - 10
    max_node = nodes    # Initialize max nodes
    for comp in netlist:    # Adds 1 to max node for each voltage source, current source max node stays the same
        if (comp[COMP.TYPE] == COMP.VS):
            max_node = max_node + 1
        if (comp[COMP.TYPE] == COMP.IS):
            max_node = max_node
    print(' Nodes ', nodes, ' total Nodes ', max_node)
    return nodes,max_node

############################################################
# Function to stamp the components into the netlist        #
############################################################

def stamper(y_add,netlist,currents,voltages,num_nodes): # pass in the netlist and matrices
    # y_add is the matrix of admittances
    # netlist is the list of lists to analyze
    # currents is the vector of currents
    # voltages is the vector of voltages
    # num_nodes is the number of nodes
    for comp in netlist:                            # for each component...
        #print(' comp ', comp)                       # which one are we handling...
        # extract the i,j and fill in the matrix...
        # subtract 1 since node 0 is GND and it isn't included in the matrix
        if ( comp[COMP.TYPE] == COMP.R ):           # a resistor
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if (i >= 0):                            # add on the diagonal
                y_add[i,i] += 1.0 / comp[COMP.VAL]
            if (j >= 0):                            # add on the diagonal
                y_add[j, j] += 1.0 / comp[COMP.VAL]
            if (j >= 0 and i >= 0):     # Adds on the the ij components
                y_add[i, j] -= 1.0 / comp[COMP.VAL]
                y_add[j, i] -= 1.0 / comp[COMP.VAL]
        if (comp[COMP.TYPE] == COMP.VS):  # a voltage source
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if (i >= 0):    # Adds the 1 component for the voltage
                y_add[num_nodes, i] = 1
                y_add[i, num_nodes] = 1
            if (j >= 0):    # Adds the -1 component for the voltage
                y_add[num_nodes, j] = -1
                y_add[j, num_nodes] = -1
            currents[num_nodes] = comp[COMP.VAL]        # Places the voltage value in the current [counter] location
            num_nodes = num_nodes+1     # Counter for num nodes to go up for every voltage source
        if (comp[COMP.TYPE] == COMP.IS):  # a current source
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if (i >= 0):        # Stamps the current value into the current array
                currents[i] = -comp[COMP.VAL]
            if (j >= 0):
                currents[j] = comp[COMP.VAL]
    return num_nodes  # need to update with new value

############################################################
# Start the main program now...                            #
############################################################

# Read the netlist!

netlist = read_netlist()    # Read the netlist by calling read_netlist python file

nodes,max_node = ranknetlist(netlist)   # Calls to the function rank netlist to get two values nodes and max node

############################################################## Initialize the arrays for correct sizing
y_add = np.zeros(shape = (max_node, max_node),dtype = np.float)
currents = np.zeros(max_node,np.float)
voltages = np.zeros(nodes,np.float)
num_nodes = nodes
############################################################### based on nodes and max nodes

stamper(y_add,netlist,currents,voltages,num_nodes)
# Calls to the function stamper to use the netlist to add values into the array above

voltages = solve(y_add, currents) # Final solution using solve command for ax = b equation

print("Netlist File")
for index in range(len(netlist)):
    print(netlist[index])
print("-" * 60)
print("Resistance Matrix")
print(y_add)
print("-" * 60)
print("Currents", currents)
print("-" * 60)
text = ["Node {}".format(i) for i in range(1, nodes + 1)]
text.append("Node 0")
voltage_df = pd.DataFrame(voltages, index = text , columns=["Node Voltage"])
print(voltage_df)


