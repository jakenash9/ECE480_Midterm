def main():
   with open('cnf.cnf') as f:
    cnf = f.readlines()
    output_var(cnf)
    unit_clause(cnf)

    
# define the output of the cnf
def output_var(cnf):
    first = cnf[1]
    out = first[0]
    print(out)
    return out

def unit_clause(cnf):
    for x in cnf:
        print(x)

if __name__ == "__main__":
    main()