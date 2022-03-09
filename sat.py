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

    print(cnf) # print cnf array

    dpll(cnf) # call dpll algorithm


def unit_clause(cnf):
    units = []
    pos = []
    neg = []
    for x in cnf: # each line
        if len(x) == 1:
            units.append(x[0])
    for u in units:
        if u < 0: 
            neg.append(u)
            false.append(u)
        else: 
            pos.append(u)
            true.append(u)
        cnf = [x for x in cnf if u not in x] # remove satisfied clauses from array
        # remove unsat literal from clauses
        for x in cnf:
            if -u in x:
                x.remove(-u)
    return cnf, pos, neg

def pure(cnf, pos, neg): # check to see if a literal appears as ALWAYS positive or ALWAYS negative
    positive = []
    negative = []
    for x in cnf:
        for q in x:
            if q > 0: positive.append(q)
            if q < 0: negative.append(q)
    pOnly = []
    nOnly = []
    for x in positive:
        if -x not in negative and x not in pOnly:
            true.append(x)
            pOnly.append(x)
    for j in negative:
        if -j not in positive and j not in nOnly:
            false.append(j)
            nOnly.append(j)
    # pos, neg = pos+pOnly, neg+nOnly
    temp = []
    for i in range(len(cnf)):
        for x in cnf[i]:
            if x in pOnly+nOnly:
                if cnf[i] not in temp: temp.append(cnf[i])
    cnf = [x for x in cnf if x not in temp]
    return cnf, pos+pOnly, neg+nOnly

def dpll(cnf):
    cnf, pos, neg = unit_clause(cnf)
    print(cnf, pos, neg)
    print()
    cnf, pos, neg = pure(cnf, pos, neg)
    print(cnf)
    print(true, false)
    if len(cnf) == 0: return True
    for x in cnf:
        if len(x) == 0 : return False

    




    

if __name__ == "__main__":
    main()