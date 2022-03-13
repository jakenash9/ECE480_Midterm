import sys
import copy
import numpy as np

def main():
    # create an output file for all possible outcomes
    temp = open("out.txt", "w")
    temp.write("")
    temp.close()
    count = 0 # number of satisfied outputs
    while True:
        output = sat() # call sat methods
        # if sat returns true, increase count
        if output:
            count +=1 # add to number of satisfied outputs
            addStr = "" # inverted set of literals put into cnf
            outStr = "" # satisfiable literals 
            # for every value in the true array
            for x in output[0]:
                outStr += " "+str(x) # add to output string
                addStr += " "+str(-x) # add inverted value to string appended to cnf
            # for every value in the false array
            for x in output[1]:
                outStr += " "+str(x) # add to output string
                addStr += " "+str(-x) # add inverted value to string appended to cnf
            # add 0 to end of strings 
            outStr += " 0\n"
            addStr += " 0\n"

            # out.cnf = output of cnf.py
            temp = open("out.cnf", "a") # open 'out.cnf' for appending
            temp.write(addStr[1:]) # append inverted string of SAT literals to 'out.cnf'
            temp.close()

            # out.txt = output of all possible solutions
            temp = open("out.txt", "a") # open 'out.txt' for appending
            temp.write(outStr[1:]) # append string of SAT literals to 'out.txt'
            temp.close()

        else:
            # if no satisfied outputs are found, print "UNSAT" and return
            if count==0:
                print("UNSAT")
            return


def sat():
    
    ################################################
    # NOTE: to run test cases
    # 1) make sat main
    # 2) inFile = open("test_cases\{FILE NAME}", "r")
    # 3) comment out 'return true, false' at the bottom of this method
    ################################################

    # read input from out.cnf
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
    # print(cnf)
    # print inputted cnf array 
    # print("CONJUNCTIVE NORMAL FORM ARRAY")
    # print("---------------------------------")
    # print(cnf) 
    # print("---------------------------------")
    # print()
    
    if dpll(cnf):
        print("SAT")
        print("True Literals: " , true)
        print("False Literals: " , false)
        print()
        return true, false # comment out to run test cnf test cases
    else:
        return False

# unit propagation clause - based on sudo code from DPLL Wikipedia
def unit_clause(cnf):
    # define arrays
    units = [] # array of unit clauses
    pos = [] # array of positive literals
    neg = [] # array of negative literals
    for x in cnf: # each line in cnf.cnf
        # check if it is a unit clause and if so, add it to units array
        if len(x) == 1 and x[0]:
            units.append(x[0])
    
    for u in units: # each unit clause (standalone literal)
        # if unit literal is negative, add to neg and false arrays
        if u < 0: 
            neg.append(u)
            false.append(u)
        # if unit literal is positive, add to pos and true arrays
        else: 
            pos.append(u)
            true.append(u)
    for u in units:
        for x in cnf:
            if -u in x:
                x.remove(-u)
    for u in units:
        # print(cnf)
        cnf = [x for x in cnf if u not in x] # remove SAT clauses from cnf array
        # remove UNSAT literal from clauses in cnf array
    
    out = []
    for x in cnf:
        if x not in out:
            out.append(x)

    return out, pos, neg # return cnf array, pos unit literal array, neg unit literal array

# pure literal elimination method - based on sudo code from DPLL Wikipedia
# checks to see if a literal appears as ALWAYS positive or ALWAYS negative
def pure(cnf, pos, neg):
    if len(cnf)==0:
        return cnf, pos, neg
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

            if x in pOnly+pos or x in nOnly+neg: # if literal only appears as positive or negative
                # add clauses with literals from pOnly or nOnly to temperary array
                if cnf[i] not in temp: 
                    temp.append(cnf[i])

    cnf = [x for x in cnf if x not in temp] # remove SAT clauses from cnf array

    # return current cnf, positive satisifed literals, negative satisfied literals
    return cnf, pos+pOnly, neg+nOnly

def dpll(cnf):
    # remove any duplicates in cnf
    res = []
    [res.append(x) for x in cnf if x not in res]
    cnf = res
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
    # two copies of current version of cnf array
    posCopy = copy.deepcopy(cnf)
    negCopy = copy.deepcopy(cnf)
    # add lowest value of newLit to copies of current version of cnf (+ and -)
    posCopy.append([newLit[0]])
    negCopy.append([-newLit[0]])

    # recursive call with new appended cnfs 
    if dpll(posCopy): # SATISFIABLE
        return True
    elif dpll(negCopy): # SATISFIABLE
        return True
    else: 
        # for each positive literal, remove from true array
        for i in pos:
                true.remove(i)
        # for each negative literal, remove from false array 
        for i in neg:
                false.remove(i)
        return False # UNSATISFIABLE

# main method run
if __name__ == "__main__":
    main()
    # sat() # for running cnf test cases