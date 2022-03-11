from re import X
import sys

def main():
    x = str(sys.argv[1]) # take SOP input
    f_or = x.split("+") # split input at OR gates
    print("split at OR gates")
    print(f_or)
    print("------------------------")
    lits_array = [] # create new array for literals
    lits = []


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
                print("poop")
                # not_gate(k, )






  


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