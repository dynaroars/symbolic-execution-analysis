from util import *
import cvc5.pythonic as cvc5

# Try cvc5 vs z3 vs dReal
# Open Github issues to discuss about runtime variety
# gurobi - LP constrain

# Capture statistics

def main():
    # Different number of nodes per layer
    # run_random(cvc5, [5, 10, 10, 5])
    # run_random(cvc5, [5, 15, 15, 5])
    # run_random(cvc5, [5, 20, 20, 5])
    # run_random(cvc5, [5, 25, 25, 5])

    # Different number of layers
    run_random(cvc5, [5, 8, 5], [-2, 2])
    run_random(cvc5, [5, 8, 8, 5], [-2, 2])
    run_random(cvc5, [5, 8, 8, 8, 5], [-2, 2])
    run_random(cvc5, [5, 25, 25, 25, 25, 5], [-2, 2])

    # Run part of ACAS Xu
    run_acasxu(cvc5) # Entire ACAS Xu
    run_acasxu(cvc5, 3) # 3 hidden layers
    run_acasxu(cvc5, 4) # 4 hidden layers

if __name__ == '__main__':
    main()
