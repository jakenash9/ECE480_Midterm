import sys

def main():
    inFile = open("cnf.cnf", "r")
    allLines = inFile.readlines()
    clauses = 0
    variables = 0
    cnf = []
    global true, false
    true = []
    false = []
    for x in allLines:
        if x[0]=='c':
            continue
        if x[0]=="p":
            temp = x.split()
            variables = int(temp[2])
            clauses = int(temp[3])
        else:
            temp = x[:len(x)-2].split()
            # print(temp)
            for t in range(len(temp)):
                temp[t]=int(temp[t])
            cnf.append(temp)
    # print(clauses, variables)
    print(cnf)
    dpll(cnf)
#    with open('cnf.cnf') as f:
#     cnf = f.readlines()
#     # print(cnf)
#     output_var(cnf)
#     cnf_small = cnf[2:]
#     unit_clause(cnf_small)
#     print(cnf_small[0])

    
# define the output of the cnf
def output_var(cnf):
    first = cnf[1]
    out = first[0]
    print(out)
    return out

def unit_clause(cnf):
    units = []
    pos = []
    neg = []
    for x in cnf: # each line
        if len(x) == 1:
            units.append(x[0])
    for u in units:
        if u < 0: neg.append(u)
        else: pos.append(u)
        cnf = [x for x in cnf if u not in x] # remove satisfied clauses from array
        # remove unsat literal from clauses
        for x in cnf:
            if -u in x:
                x.remove(-u)
    return cnf, pos, neg

def dpll(cnf):
    cnf, pos, neg = unit_clause(cnf)
    print(cnf, pos, neg)



    

if __name__ == "__main__":
    main()