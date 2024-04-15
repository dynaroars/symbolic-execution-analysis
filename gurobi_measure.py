import gurobipy as gp
from keras.models import Sequential
from keras.layers import Dense
from symbolic_execution import generate_symbolic_execution, create_random
import time

def get_info(layer: Dense):
    """
    Extract weights and bias from a layer
    """
    weights = layer.kernel_initializer.value
    bias = layer.bias_initializer.value
    return (weights, bias)

def gurobi_read_spec(var_dict, model: gp.Model, filename="acasxu/spec/prop_1.vnnlib"):
    file = open(filename)

    for line in file:
        line = line.strip()

        # Skip empty or comment lines
        if line == "" or line.startswith(";"):
            continue

        line = line[1:-1]
        if line.startswith("declare-const"):
            continue
        elif line.startswith("assert"):
            op, variable_name, value = line[8:-1].split()
            if value.startswith("X") or value.startswith("Y"):
                value = var_dict[value]
            else:
                value = eval(value)
            if op == ">=":
                model.addConstr(var_dict[variable_name] >= value)
            elif op == "<=":
                print(model.getVars())
                print(variable_name)
                model.addConstr(var_dict[variable_name] <= value)

    file.close()

def gurobi_generate_symbolic_execution(dnn: Sequential, model: gp.Model):
    """
    Return symbolic states from a dnn following the format of given library
    Args:
        dnn (type: Sequential)
        library (e.g. z3, cvc5)
    """
    layers = dnn.layers

    # Extract info from the first layer to define a list of inputs
    first_layer = layers[0]
    weights, _ = get_info(first_layer)
    num_inputs = len(weights)
    input_list = []
    output_list = []
    var_dict = {}

    for i in range(num_inputs):
        var_name = 'X_' + str(i)
        v = model.addVar(vtype='C', lb = -gp.GRB.INFINITY, name=var_name)
        input_list.append(v)
        var_dict[var_name] = v

    # Iterate through layers to determine the neurons in each layer
    for index in range(len(layers) - 1):
        # Get the layer info
        layer = layers[index]
        weights, bias = get_info(layer)
        num_neurons = len(weights[0])

        # Define the neuron list
        neuron_list = [model.addVar(vtype='C', lb = -gp.GRB.INFINITY, name='n' + str(index) + '_' + str(x)) for x in range(num_neurons)]
        for i in range(len(neuron_list)):
            # Find the sum weights of a neuron
            total = weights[0][i] * input_list[0]
            for input in range(1, len(input_list)):
                total += (weights[input][i] * input_list[input])

            # Add bias and clean up the formula
            total += bias[i][0]

            t = model.addVar(vtype='C', lb = -gp.GRB.INFINITY)
            model.addConstr(t == total)
            # total = library.simplify(total)
            # Append the constraint into the list
            model.addGenConstrMin(neuron_list[i], [t, 0])

        # The current neuron list becomes the inputs for the next layer
        input_list = neuron_list

    # Extract info from the last layer to define a list of outputs
    last_layer = layers[-1]
    weights, bias = get_info(last_layer)
    num_outputs = len(weights[0])

    for i in range(num_outputs):
        var_name = 'Y_' + str(i)
        v = model.addVar(vtype='C', lb = -gp.GRB.INFINITY, name=var_name)
        output_list.append(v)
        var_dict[var_name] = v

    for i in range(len(output_list)):
        # Find the sum weights of the final outputs
        total = weights[0][i] * input_list[0]
        for input in range(1, len(input_list)):
            total += (weights[input][i] * input_list[input])
        total += bias[i][0]
        # total = library.simplify(total)

        # Append the outputs into the list
        model.addConstr(output_list[i] == total)

    return var_dict
dnn = create_random([5, 25, 25, 25, 25, 5])

t = []
for i in range(1):
    model = gp.Model()
    model.Params.TimeLimit = 20
    var_dict = gurobi_generate_symbolic_execution(dnn, model)
    gurobi_read_spec(var_dict, model)
    start = time.time()
    model.optimize()
    t.append(time.time() - start)
    print(model.SolCount)
    model.display()
