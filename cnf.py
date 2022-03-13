
import sys

def main():
    x = str(sys.argv[1]) # take SOP input
    f_or = x.split("+") # split input at OR gates
    print("split at OR gates")
    print(f_or)
    print("------------------------")
    lits_array = [] # create new array for literals
    output = []
    counter, lit = var_count(x)


    # for each clause in f_or split at AND gates and append to lits
    for x in f_or:
        f_and = x.split(".")
        lits_array.append(f_and)

    print("split at AND gates")    
    print(lits_array)
    print("------------------------")
    # for each literal in nested array of literal
    for j in lits_array:
        for i,k in enumerate(j): # index of each literal in each array
            # find not gate and call not_gate function
            if k[0] == "~":
                output.append(not_gate(k, "x" + str(counter))) # add not gate to output
                j[i]="x"+str(counter) # replace not gates with new output
                counter +=1
    print("NOT gates removed")
    print(lits_array)
    print("------------------------")
    

    # for each AND gate
    for j in lits_array:
        # find 2 input AND gates from left to right
        while len(j)>1:
            k = j[0]+"."+j[1]
            # call and_gate with first 2 literals left to right and append to output
            output.append(and_gate(k, "x" + str(counter)))
            # remove first 2 literals from j after they are ANDed
            j.pop(0)
            j.pop(0)
            j.insert(0,"x" + str(counter)) # insert output of and_gate in place of the two inputs 
            counter += 1 # increase highest literal count

    # for each OR gate
    while len(lits_array)>1:
        k = lits_array[0][0]+"+"+lits_array[1][0] # combine first two literals into a new string
        # call or_gate with first two literals left to right and append to output
        output.append(or_gate(k, "x" + str(counter))) 
        # remove first two literals from lits_array after they are ORed
        lits_array.pop(0)
        lits_array.pop(0)
        lits_array.insert(0,["x" + str(counter)]) # insert output of or_gate in place of two inputs
        counter += 1 # increase highest literal count

        # array now holds the highest single literal, representing the output of the entire function 
    
    
    output.append(lits_array[0][0][1:]+" 0\n") # append highest literal to output array
    sec = [j.split("\n") for j in output] # remove "\n" from array
    clause_len = 0 # variable to hold number of clauses
    # for each line in sec array
    for j in sec:
        clause_len+=len(j)-1 # number of lines in cnf file (clauses)
    # insert cnf header into output file: p cnf {number of clauses} {output literal number}
    output.insert(0, "p cnf "+ str(clause_len) + " " + str(counter-1)+"\n")
    print(output)
    outFile = open("out.cnf", "w") # create output file to write to

    # for each element in the output array, write to cnf output file 
    for x in output:
        outFile.write(x)
    outFile.close()

    # # EXAMPLE FOR NICK DELETE WHEN DONE!!!!!!!!!!!!!!!
    # temp = "~x1"
    # not_gate(temp, "x2")


def var_count(f):
    ors = f.split("+") # split by OR gates
    lits = [] # array of literals
    count = -1 # count for highest literal
    # for each AND clause
    for x in ors:
        ands = x.split(".") # split into literals
        # for each literal
        for i in ands:
            # if literal has a NOT, remove it (don't need negative for counting)
            if i.find("~") != -1:
                i = i[1:]
            # if literal is not already in lits array, add it
            if i not in lits:
                lits.append(i)
    # for each literal number 
    for j in lits:
        numLit = int(j[1:])
        # if current literal number is higher than count, make count = current literal
        if numLit > count:
            count = numLit
    
    return count+1, lits # return highest count+1 for new output, and lits array


  

# AND gate method based on AND formula from lecture
def and_gate(f,out):
    func = f.split(".")
    return func[0][1:]+" -"+out[1:]+" 0\n"+func[1][1:]+" -"+out[1:]+" 0\n"+"-"+func[0][1:]+" -"+func[1][1:]+" "+out[1:]+" 0\n"

# OR gate method based on OR formula from lecture
def or_gate(f,out):
    func = f.split("+")
    return "-" + func[0][1:] + " " + out[1:] + " 0\n" + "-" + func[1][1:] + " " + out[1:] + " 0\n" + func[0][1:] + " " + func[1][1:] + " -" + out[1:] + " 0\n"

# NOT gate method based on NOT formula from lecture  
def not_gate(f, out):
    func = f.split("~")
    # print()
    # print("NOT GATE EXAMPLE: f ='~x1' and out = 'x2'")
    # print(func)
    # print(func[1])
    # print(func[1][1:])
    # print("-" + func[1][1:] + " -" + out[1:] + " 0\n")
    # print(func[1][1:] + " " + out[1:] + " 0\n")
    return "-" + func[1][1:] + " -" + out[1:] + " 0\n" + func[1][1:] + " " + out[1:] + " 0\n"

if __name__ == "__main__":
    main()