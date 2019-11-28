import numpy as np
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x):
    return x * (1 - x)


class NN:
    def __init__(self, hiddenLayers):
        self.w1 = 2 * np.random.random((7, hiddenLayers)) - 1
        self.w2 = 2 * np.random.random((hiddenLayers, 10)) - 1

    def train(self, training_inputs, training_outputs, iterations):
        for it in range(iterations):
            output = self.think(training_inputs)
            error = training_outputs - output
            adjustments = np.dot(self.layer.T, error * sigmoid_derivative(output))
            self.w2 += adjustments
            adjustments = np.dot(training_inputs.T,
                                 np.dot(error * sigmoid_derivative(output), self.w2.T) *
                                 sigmoid_derivative(self.layer))
            self.w1 += adjustments

    def think(self, inputs):
        inputs = inputs.astype(float)
        self.layer = sigmoid(np.dot(inputs, self.w1))
        output = sigmoid(np.dot(self.layer, self.w2))
        return output

    def recognize(self, inputs):
        out = self.think(inputs)
        return np.argwhere(out == np.max(out))[0][0]


def readFromFile():
    f = open("segments.data", "r")
    ret_X = []
    ret_y = []
    for line in f:
        chs_X = []
        chs_y = []
        for ch in line:
            if ch not in [",", " ", "\n"]:
                if len(chs_X) < 7:
                    chs_X.append(int(ch))
                else:
                    chs_y.append(int(ch))
        ret_X.append(chs_X)
        ret_y.append(chs_y)
    return ret_X, ret_y


if __name__ == "__main__":
    a, b = readFromFile()
    rn = NN(10)

    inputs = np.array(a)
    outputs = np.array(b)
    running = True
    while running:
        order = input("train / see / exit\n")
        if order == "exit":
            running = False
        elif order == "train":
            times = int(input("Number of training sesions?"))
            rn.train(inputs, outputs, times)
        elif order == "see":
            testData = np.array(input("Date intrare (7 biti cu virgula intre ele):\n").split(",")).astype(int)
            print(np.round(rn.think(testData), decimals=3))
            print(rn.recognize(testData))
        else:
            print("nu stiu comanda\n")
