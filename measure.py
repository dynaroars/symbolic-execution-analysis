from util import my_symbolic_execution, create_random
from acasxu import read_spec, readNNet
import time
import z3

# Capture statistics
REPETITION = 5
TIMEOUT = 1800 * 6 * 1000 # Set timeout of 30 minutes

def run_random(layers: [int], interval: [int] = [-5, 5]):
    output_file = open("runtime.txt", "a")
    output_file.write(f"layers = {layers}, interval = {interval}\n")
    total = 0
    for _ in range(REPETITION):
        dnn = create_random(layers, interval)
        symbolic_states = my_symbolic_execution(dnn)
        pre, post = read_spec("acasxu/spec/prop_1.vnnlib")
        f = z3.And([symbolic_states, pre, post])
        solver = z3.Solver()
        solver.set("timeout", TIMEOUT)
        solver.add(f)

        # Calculate the solving time
        start = time.time()
        result = solver.check()
        duration = time.time() - start
        total += duration
        output_file.write(f"{result}, {duration}\n")

    output_file.write(f"total: {total}, average: {total / REPETITION}\n")
    output_file.write("----------------------------\n\n")
    output_file.close()

def run_acasxu():
    output_file = open("runtime.txt", "a")
    output_file.write(f"ACASXU\n")

    dnn = readNNet("acasxu/nnet/ACASXU_run2a_1_1_batch_2000.nnet")
    states = my_symbolic_execution(dnn)
    pre, post = read_spec("acasxu/spec/prop_1.vnnlib")
    f = z3.And([states, pre, post])
    solver = z3.Solver()
    solver.set("timeout", TIMEOUT)
    solver.add(f)

    start = time.time()
    result = solver.check()
    duration = time.time() - start
    output_file.write(f"{result}, {duration}\n")
    output_file.write("----------------------------\n\n")

    output_file.close()

def run_part_acasxu(filename):
    output_file = open("runtime.txt", "a")
    output_file.write(f"ACASXU-{filename}\n")

    dnn = readNNet(filename)
    states = my_symbolic_execution(dnn)
    pre, post = read_spec("acasxu/spec/prop_1.vnnlib")
    f = z3.And([states, pre, post])
    solver = z3.Solver()
    solver.set("timeout", TIMEOUT)
    solver.add(f)

    start = time.time()
    result = solver.check()
    duration = time.time() - start
    output_file.write(f"{result}, {duration}\n")
    output_file.write("----------------------------\n\n")

    output_file.close()

def main():
    # Different number of nodes per layer
    # run_random([5, 10, 10, 5], [-2, 2])
    # run_random([5, 20, 20, 5], [-2, 2])
    # run_random([5, 30, 30, 5], [-2, 2])
    # run_random([5, 40, 40, 5], [-2, 2])

    # Different number of layers
    # run_random([5, 15, 5], [-2, 2])
    # run_random([5, 15, 15, 5], [-2, 2])
    # run_random([5, 15, 15, 15, 5], [-2, 2])
    # run_random([5, 15, 15, 15, 15, 5], [-2, 2])

    # Different random interval
    # run_random([5, 15, 15, 5], [-2, 2])
    # run_random([5, 15, 15, 5], [-5, 5])
    # run_random([5, 15, 15, 5], [-10, 10])
    # run_random([5, 15, 15, 5], [-15, 15])

    # Check ACAS Xu
    # run_acasxu()

    # Run part of ACAS Xu
    run_part_acasxu("acasxu/small-makeup.nnet")
    run_part_acasxu("acasxu/big-makeup.nnet")

if __name__ == '__main__':
    main()
