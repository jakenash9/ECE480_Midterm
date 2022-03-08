import sys

def main():
   with open('cnf.cnf') as f:
    cnf = f.readlines()
    # print(cnf)
    output_var(cnf)
    cnf_small = cnf[2:]
    unit_clause(cnf_small)
    print(cnf_small[0])

    
# define the output of the cnf
def output_var(cnf):
    first = cnf[1]
    out = first[0]
    print(out)
    return out

def unit_clause(cnf_small):
    for x in cnf_small: # each line
        for k in x: # each number
            print("idk")
            


    

if __name__ == "__main__":
    main()