
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
        for k in j:
            # find not gate and call not_gate function
            if k[0] == "~":
                print(k)
                output.append(not_gate(k, "x" + str(counter)))
                counter +=1

    print(output, "OUT")
    print(output[0])
    print(not_gate("~x4", "x5"))

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


  


def and_gate(f,out):
    func = f.split(".")
    return func[0][1:]+" -"+out[1:]+"\n"+func[1][1:]+" -"+out[1:]+"\n"+"-"+func[0][1:]+" -"+func[1][1:]+" "+out[1:]+"\n"

def or_gate(f,out):
    func = f.split("+")
    return "-" + func[0][1:] + " " + out[1:] + "\n" + "-" + func[1][1:] + " " + out[1:] + "\n" + func[0][1:] + " " + func[1][1:] + " -" + out[1:] + "\n"
    
def not_gate(f, out):
    func = f.split("~")
    return "-" + func[1][1:] + " -" + out[1:] + "\n" + func[1][1:] + " " + out[1:] + "\n"

if __name__ == "__main__":
    main()