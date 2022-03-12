import sys
import copy
import numpy as np

def main():
    # read input from cnf.cnf
    inFile = open("out.cnf", "r")
    # Array of cnf lines
    allLines = inFile.readlines()
    # initializing variables
    clauses = 0
    variables = 0
    # define empty arrays
    cnf = [] # array of arrays of clauses
    global true, false
    true = [] # global array of true values
    false = [] # global array of false values
    for x in allLines:
        if x[0]=='c': # check for comment
            continue
        if x[0]=="p": # check for cnf header 
            temp = x.split() # split at pance
            variables = int(temp[2]) # number of variables
            clauses = int(temp[3]) # number or clauses
        else:
            temp = x[:len(x)-2].split() # temperary arrays of each clause
            # parse each literal and add to cnf array
            for t in range(len(temp)):
                temp[t]=int(temp[t])
            cnf.append(temp)
    # print inputted cnf array 
    # print("CONJUNCTIVE NORMAL FORM ARRAY")
    # print("---------------------------------")
    # print(cnf) 
    # print("---------------------------------")
    # print()
    
    if dpll(cnf) == True:
        print("SAT")
    else:
        print("UNSAT")

# unit propagation clause - based on sudo code from DPLL Wikipedia
def unit_clause(cnf):
    print(cnf)
    # define arrays
    units = [] # array of unit clauses
    pos = [] # array of positive literals
    neg = [] # array of negative literals
    for x in cnf: # each line in cnf.cnf
        # check if it is a unit clause and if so, add it to units array
        if len(x) == 1 and x[0]:
            units.append(x[0])
    print(units, "asdfasdfasdf")
    for u in units: # each unit clause (standalone literal)
        # if unit literal is negative, add to neg and false arrays
        if u < 0: 
            if u not in neg: neg.append(u)
            if u not in false: false.append(u)
        # if unit literal is positive, add to pos and true arrays
        else: 
            if u not in pos: pos.append(u)
            if u not in true: true.append(u)
        cnf = [x for x in cnf if u not in x] # remove SAT clauses from cnf array
        # remove UNSAT literal from clauses in cnf array
        for x in cnf:
            if -u in x:
                x.remove(-u)
    return cnf, pos, neg # return cnf array, pos unit literal array, neg unit literal array

# pure literal elimination method - based on sudo code from DPLL Wikipedia
# checks to see if a literal appears as ALWAYS positive or ALWAYS negative
def pure(cnf, pos, neg):
    # define positive and negative arrays after unit clauses removed
    positive = [] # positive literals 
    negative = [] # negative literals

    for x in cnf: # each clause in cnf after disgarded unit clauses
        for q in x: # sort each literal into positive and negative arrayy
            if q > 0: positive.append(q)
            if q < 0: negative.append(q)

    # define pOnly and nOnly arrays
    pOnly = [] # literals that only appear positive
    nOnly = []  # literals that only appear negative

    for x in positive: # each positive literal
        # if a positive literal never appears negative, set to true and add to pOnly array
        if -x not in negative and x not in pOnly:
            true.append(x)
            pOnly.append(x)
    for j in negative: # each negative literal
        # if a negative literal never appears positive, set to false and add to nOnly array
        if -j not in positive and j not in nOnly:
            false.append(j)
            nOnly.append(j)
    temp = []
    for i in range(len(cnf)): # for each clause - range allows for us to edit the array in this loop
        for x in cnf[i]: # each literal
            if x in pOnly+nOnly: # if literal only appears as positive or negative
                # add clauses with literals from pOnly or nOnly to temperary array
                if cnf[i] not in temp: 
                    temp.append(cnf[i])

    cnf = [x for x in cnf if x not in temp] # remove SAT clauses from cnf array
    # return current cnf, positive satisifed literals, negative satisfied literals
    return cnf, pos+pOnly, neg+nOnly

def dpll(cnf):
    # send cnf array through unit propagation clause 
    cnf, pos, neg = unit_clause(cnf)

    # # print cnf, positive unit literals, and negative unit literals after unit_clause
    # print("CNF (NO UNIT CLAUSES), POS UNIT CLAUSES, NEG UNIT CLAUSES")
    # print("---------------------------------")
    # print(cnf, pos, neg)
    # print("---------------------------------")
    # print()

    # # send cnf, pos, and neg arrays through pure literal elimination
    cnf, pos, neg = pure(cnf, pos, neg)

    # # print cnf, positive satisfied literals, and negative satisfied literals after pure
    # print("CNF (NO PURE LITERALS), TRUE LITERALS, FALSE LITERALS")
    # print("---------------------------------")
    # print(cnf, true, false)
    # print("---------------------------------")
    # print()

    newLit = []
    if len(cnf) == 0:
        return True # if cnf is empty return true (SAT)
    temp = False
    # if an empty clause is found set temp to True 
    for x in cnf:
        if len(x) == 0 : temp = True
        else: 
            for k in x: # each literal in cnf
                # add absolute value of each literal to a new array
                if abs(k) not in newLit:
                    newLit.append(abs(k))
    newLit = sorted(newLit) # sort the list from smallest to largest literal

    # if an empty clause is found...
    if temp:
        # remove all values in pos array from true array
        for i in pos: 
            true.remove(i)
        # remove all values in neg array from false array
        for i in neg:
            false.remove(i)
        return False # return false (UNSAT)

    # allocate memory for two copies of current version of cnf array
    posCopy = copy.deepcopy(cnf)
    negCopy = copy.deepcopy(cnf)
    # add lowest value of newLit to copies of current version of cnf (+ and -)
    posCopy.append([newLit[0]])
    negCopy.append([-newLit[0]])

    # recursive call with new appended cnfs 
    if dpll(posCopy): # SATISFIABLE
        print("TRUE, 2")
        return True
    elif dpll(negCopy): # UNSATISFIABLE
        print("FALSE, 2")
        return False
    else: 
        # for each positive literal, remove from true array
        for i in pos:
                true.remove(i)
        # for each negative literal, remove from false array 
        for i in neg:
                false.remove(i)
        print("FALSE, 3")
        return False # UNSATISFIABLE

# main method run
if __name__ == "__main__":
    main()