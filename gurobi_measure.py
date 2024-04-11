import gurobipy as gp
from keras.models import Sequential
from keras.layers import Dense
from symbolic_execution import generate_symbolic_execution, create_random
import time

m = gp.Model()
a = m.addVar(vtype="C", lb = -gp.GRB.INFINITY, name = "a")
b = m.addVar(vtype="C", lb = -gp.GRB.INFINITY, name = "b")
c = m.addVar(vtype="C", lb = -gp.GRB.INFINITY, name = "c")
t = m.addVar(vtype="C", lb = -gp.GRB.INFINITY, name = "t")

# m.addConstr(t == a + b)
# m.addConstr(c == gp.min_(t, -10))
print(type(t == a + b))
print(type(gp.and_(t == a + b, t == a + c)))
print(m.addConstr(t == a + b & t == a + c))

m.optimize()
m.display()

for v in m.getVars():
    print('%s %g' % (v.VarName, v.X))

# def get_info(layer: Dense):
#     """
#     Extract weights and bias from a layer
#     """
#     weights = layer.kernel_initializer.value
#     bias = layer.bias_initializer.value
#     return (weights, bias)

# def my_generate_symbolic_execution(dnn: Sequential, model: gp.Model):
#     """
#     Return symbolic states from a dnn following the format of given library
#     Args:
#         dnn (type: Sequential)
#         library (e.g. z3, cvc5)
#     """
#     layers = dnn.layers

#     # Extract info from the first layer to define a list of inputs
#     first_layer = layers[0]
#     weights, _ = get_info(first_layer)
#     num_inputs = len(weights)
#     input_list = [model.addVar(vtype='C', lb = -gp.GRB.INFINITY, name='X_' + str(i)) for i in range(num_inputs)]

#     # Iterate through layers to determine the neurons in each layer
#     for index in range(len(layers) - 1):
#         # Get the layer info
#         layer = layers[index]
#         weights, bias = get_info(layer)
#         num_neurons = len(weights[0])

#         # Define the neuron list
#         neuron_list = [model.addVar(vtype='C', lb = -gp.GRB.INFINITY, name='n' + str(index) + '_' + str(x)) for x in range(num_neurons)]
#         for i in range(len(neuron_list)):
#             # Find the sum weights of a neuron
#             total = weights[0][i] * input_list[0]
#             for input in range(1, len(input_list)):
#                 total += (weights[input][i] * input_list[input])

#             # Add bias and clean up the formula
#             total += bias[i][0]

#             t = model.addVar(vtype='C', lb = -gp.GRB.INFINITY)
#             model.addConstr(t == total)
#             # total = library.simplify(total)
#             # Append the constraint into the list
#             model.addGenConstrMin(neuron_list[i], [t, 0])

#         # The current neuron list becomes the inputs for the next layer
#         input_list = neuron_list

#     # Extract info from the last layer to define a list of outputs
#     last_layer = layers[-1]
#     weights, bias = get_info(last_layer)
#     num_outputs = len(weights[0])
#     output_list = [model.addVar(vtype='C', lb = -gp.GRB.INFINITY,  name='Y_' + str(i)) for i in range(num_outputs)]

#     for i in range(len(output_list)):
#         # Find the sum weights of the final outputs
#         total = weights[0][i] * input_list[0]
#         for input in range(1, len(input_list)):
#             total += (weights[input][i] * input_list[input])
#         total += bias[i][0]
#         # total = library.simplify(total)

#         # Append the outputs into the list
#         model.addConstr(output_list[i] == total)

# dnn = create_random([5, 25, 25, 25, 25, 5])

# t = []
# for i in range(2):
#     model = gp.Model()
#     model.Params.TimeLimit = 2
#     my_generate_symbolic_execution(dnn, model)
#     start = time.time()
#     model.optimize()
#     t.append(time.time() - start)
#     print(model.SolCount)
    # states = generate_symbolic_execution(dnn, z3)
    # for v in model.getVars():
    #     print('%s %g' % (v.VarName, v.X))

