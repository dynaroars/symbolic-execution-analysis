from symbolic_execution import generate_symbolic_execution, create_random
from acasxu import read_spec, readNNet
import time

REPETITION = 5
TIMEOUT = 3600 * 1000 # Set timeout of 30 minutes

def run_random(library, layers, interval = [-5, 5]):
    output_file = open("runtime.txt", "a")
    output_file.write(f"library = {library.__name__}, layers = {layers}, interval = {interval}\n")
    total = 0
    count = 0
    while count < REPETITION:
        dnn = create_random(layers, interval)
        symbolic_states = generate_symbolic_execution(dnn, library)
        pre, post = read_spec(library, "acasxu/spec/prop_1.vnnlib")
        symbolic_expr = library.And([symbolic_states, pre, post])
        result, duration = solve_model(library, symbolic_expr)

        if result == "sat":
            continue

        count += 1
        # Repeat the same random DNN to make sure the runtime doesn't vary too much
        runtimes = [duration]
        for _ in range(4):
            _, duration = solve_model(library, symbolic_expr)
            runtimes.append(duration)

        total += sum(runtimes) / len(runtimes)
        runtimes = [str(i) for i in runtimes]
        output_file.write(f"{result}, {'--'.join(runtimes)}\n")

    output_file.write(f"total: {total}, average: {total / REPETITION}\n")
    output_file.write("----------------------------\n\n")
    output_file.close()

def run_acasxu(library):
    output_file = open("runtime.txt", "a")
    output_file.write(f"library = {library.__name__}, ACASXU\n")

    dnn = readNNet("acasxu/nnet/ACASXU_run2a_1_1_batch_2000.nnet")
    states = generate_symbolic_execution(dnn)
    pre, post = read_spec("acasxu/spec/prop_1.vnnlib")
    f = library.And([states, pre, post])
    result, duration = solve_model(library, f)
    output_file.write(f"{result}, {duration}\n")
    output_file.write("----------------------------\n\n")

    output_file.close()

def solve_model(library, symbolic_expression):
    solver = library.Solver()
    solver.add(symbolic_expression)
    start = time.time()
    result = solver.check()
    duration = time.time() - start
    return result, duration    

def run_part_acasxu(library, filename):
    output_file = open("runtime.txt", "a")
    output_file.write(f"library = {library.__name__}, ACASXU-{filename}\n")

    dnn = readNNet(filename)
    states = generate_symbolic_execution(dnn)
    pre, post = read_spec("acasxu/spec/prop_1.vnnlib")
    f = library.And([states, pre, post])
    result, duration = solve_model(library, f)
    output_file.write(f"{result}, {duration}\n")
    output_file.write("----------------------------\n\n")

    output_file.close()
