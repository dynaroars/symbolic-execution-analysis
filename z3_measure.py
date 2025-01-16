from util import *
import z3

# Try cvc5 vs z3 vs dReal
# Open Github issues to discuss about runtime variety
# gurobi - LP constrain

# Capture statistics

def main():
    # Different number of nodes per layer
    # run_random(z3, [5, 10, 10, 5])
    # run_random(z3, [5, 15, 15, 5])
    # run_random(z3, [5, 20, 20, 5])
    # run_random(z3, [5, 25, 25, 5])

    # Different number of layers
    run_random(z3, [5, 8, 5], [-2, 2])
    run_random(z3, [5, 8, 8, 5], [-2, 2])
    run_random(z3, [5, 8, 8, 8, 5], [-2, 2])
    run_random(z3, [5, 25, 25, 25, 25, 5], [-2, 2])

    # Run part of ACAS Xu
    run_acasxu(z3, 3) # 3 hidden layers
    # run_acasxu(z3, 4) # 4 hidden layers
    # run_acasxu(z3) # Entire ACAS Xu

if __name__ == '__main__':
    main()
