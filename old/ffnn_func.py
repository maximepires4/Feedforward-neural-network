import numpy as np
import matplotlib.pyplot as plt

GRAPH_MIN = -1
GRAPH_MAX = 6


def arrayB(array):
    # Calculate a new array with a column of ones based on the input array
    if array.ndim == 1:
        arrayB = np.zeros((array.shape[0], 2))
        for i in range(array.shape[0]):
            arrayB[i, 0] = 1
            arrayB[i, 1:] = array[i]
        return arrayB
    arrayB = np.zeros((array.shape[0], array.shape[1]+1))
    for i in range(array.shape[0]):
        arrayB[i, 0] = 1
        arrayB[i, 1:] = array[i, :]

    return arrayB


def doForwardPropagation(Xb, Y, v, w):
    # Forward propagation algorithm

    Xbb = np.dot(Xb, v)
    F = sigmoid(Xbb)

    Fb = arrayB(F)

    Fbb = np.zeros((Fb.shape[0], 1))
    for i in range(Fb.shape[0]):
        Fbb[i] = 
        Fbb[i] = np.dot(Fb[i, :], w)
    #Fbb = np.dot(Fb, w)
    G = sigmoid(Fbb)

    error = np.sum((Y - G)**2)

    return F, Fb, G, error


def resolveForwardPropagation(X, v, w):
    # Forward propagation algorithm, this function is simplified when we only need to resolve for some given points

    Xb = arrayB(X)

    print("Xb")
    print(Xb)

    Xbb = np.dot(Xb, v)
    F = sigmoid(Xbb)

    print("F")
    print(F)

    Fb = np.zeros((F.shape[0], F.shape[1]+1))
    for i in range(F.shape[0]):
        Fb[i, 0] = 1
        Fb[i, 1:] = F[i, :]

    print("Fb")
    print(Fb)
    print("w")
    print(w)

    Fbb = np.zeros((Fb.shape[0], 1))
    for i in range(Fb.shape[0]):
        Fbb[i] = np.dot(Fb[i, :], w)
    #Fbb = np.dot(Fb, w)

    print("Fbb")
    print(Fbb)

    G = sigmoid(Fbb)

    return G


def sigmoid(x):
    # sigmoid function
    return 1 / (1 + np.exp(-x))


def doBackPropagation(Xb, F, Fb, G, v, w, alpha1, alpha2, Y):
    # Back propagation algorithm

    tmp = np.zeros((Y.shape[0], 1))
    for i in range(Y.shape[0]):
        tmp[i] = (Y[i] - G[i])*G[i]*(1-G[i])

    delta_w = np.dot(Fb.T, tmp)
    delta_v = np.dot(Xb.T, np.dot(tmp, w[1:, :].T)*F*(1-F))

    w = w + alpha1*delta_w
    v = v + alpha2*delta_v

    return v, w


def ffnn(X, neurons, data_y, max_iter = None, print_error = False, print_output_variable = False):
    # Feedforward neural network algorithm
    K = 4
    v = np.random.rand(X.shape[1]+1, neurons)  # 2+1 inputs / K neurons
    w = np.random.rand(neurons+1, 1)  # K+1 neurons / 3 outputs

    Y = np.array(data_y)

    # Initialize variables
    alpha1 = 0.001
    alpha2 = alpha1
    epsilon = 0.0001
    error = np.power(10, 5)
    error_old = error
    deltaError = error
    itera = 0

    Xb = arrayB(X)

    error_history = []

    # Iterate until the error is acceptable
    while np.abs(deltaError) > epsilon:
        itera = itera + 1
        F, Fb, G, error = doForwardPropagation(Xb, Y, v, w)
        v, w = doBackPropagation(Xb, F, Fb, G, v, w, alpha1, alpha2, Y)

        # Keep track of the error
        deltaError = error - error_old
        error_old = error
        error_history.append(error)

        if(itera%100 == 0):
            print("Error: {}".format(error))

        if(itera == max_iter):
            print("Warning: Maximum number of iterations reached {}".format(max_iter))
            break

    if print_error:
        print(f"Error: {error}")
        print(f"Iterations: {itera}")
        plt.figure(2)
        plt.plot(error_history)
        plt.xlabel('Iteration')
        plt.ylabel('Error')

    if print_output_variable:
        print(f"G: {G}")
        print(f"v: {v}")
        print(f"w: {w}")

    return v, w