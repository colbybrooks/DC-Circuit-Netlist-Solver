############################################################
# read netlist file and create a list of lists...          #
############################################################

import comp_constants as COMP    # get the constants needed for lists

def read_netlist():        # read a netlist - no input argument!
    filename=input("enter netlist text file name: ")        # ask for the netlist
    #print(filename)                                        # debug statement
    fh = open(filename,"r")                                 # open the file
    lines = fh.readlines()                                  # read the file

    netlist = []                                            # initialize our list
    for line in lines:                                      # for each component...
        line=line.strip()                                   # strip CR/LF
        if line:                                            # skip empty lines

            # reads: name, from, to, value
            # so we need to insert the node type at the start of the list
            properties = line.split(" ")            # parse properties delimited by blanks

            if ( properties[COMP.TYPE][0] == COMP.RESIS ):              # is it a resistor?
                properties.insert(COMP.TYPE,COMP.R)                     # Yes!
                properties[COMP.I]       = int(properties[COMP.I])      # convert from string
                properties[COMP.J]       = int(properties[COMP.J])      # convert from string
                properties[COMP.VAL]     = float(properties[COMP.VAL])  # convert from string
                netlist.append(properties)                              # add to our netlist

            elif ( properties[COMP.TYPE][0:2] == COMP.V_SRC ):          # a voltage source?
                properties.insert(COMP.TYPE,COMP.VS)                    # Yes!
                properties[COMP.I]       = int(properties[COMP.I])      # convert from string
                properties[COMP.J]       = int(properties[COMP.J])      # convert from string
                properties[COMP.VAL]     = float(properties[COMP.VAL])  # convert from string
                netlist.append(properties)                              # add to our netlist

            elif ( properties[COMP.TYPE][0:2] == COMP.I_SRC ):          # a current source?
                properties.insert(COMP.TYPE,COMP.IS)                    # Yes!
                properties[COMP.I]       = int(properties[COMP.I])      # convert from string
                properties[COMP.J]       = int(properties[COMP.J])      # convert from string
                properties[COMP.VAL]     = float(properties[COMP.VAL])  # convert from string
                netlist.append(properties)                              # add to our netlist

            else:                                                       # unknown component!
                print("Got an unknown component type:\n",line)          # bad data!
                quit()                                                  # bail!

    return netlist    # return the netlist
