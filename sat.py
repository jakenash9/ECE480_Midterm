import sys
# from tkinter.messagebox import NO

def main():
    # read input from cnf.cnf
    inFile = open("cnf.cnf", "r")
    # Array of cnf lines
    allLines = inFile.readlines()
    # initializing variables
    clauses = 0
    variables = 0
    # define empty arrays
    cnf = [] # array of arrays of clauses
    global true, false
    true = [] # array of true values
    false = [] # array of false values
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
    print("CONJUNCTIVE NORMAL FORM ARRAY")
    print("---------------------------------")
    print(cnf) 
    print("---------------------------------")
    print()

    dpll(cnf) # call dpll algorithm

# unit propagation clause - based on sudo code from DPLL Wikipedia
def unit_clause(cnf):
    # define arrays
    units = []
    pos = []
    neg = []
    for x in cnf: # each line in cnf.cnf
        # check if it is a unit clause and if so, add it to units array
        if len(x) == 1:
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

    # print cnf, positive unit literals, and negative unit literals after unit_clause
    print("CNF (NO UNIT CLAUSES), POS UNIT CLAUSES, NEG UNIT CLAUSES")
    print("---------------------------------")
    print(cnf, pos, neg)
    print("---------------------------------")
    print()

    # send cnf, pos, and neg arrays through pure literal elimination
    cnf, pos, neg = pure(cnf, pos, neg)

    # print cnf, positive satisfied literals, and negative satisfied literals after pure
    print("CNF (NO PURE LITERALS), TRUE LITERALS, FALSE LITERALS")
    print("---------------------------------")
    print(cnf, true, false)
    print("---------------------------------")
    print()

    
    if len(cnf) == 0: return True # if cnf is empty return true
    # if an empty clause is found return false 
    for x in cnf:
        if len(x) == 0 : return False

    




    

if __name__ == "__main__":
    main()