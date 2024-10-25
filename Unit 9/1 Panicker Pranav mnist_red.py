import numpy as np
import pickle
from scipy.ndimage import rotate

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))

def initialize_network(structure):
    weights, biases = [None], [None]
    for i in range(len(structure) - 1):
        biases.append(np.random.uniform(-1, 1, (1, structure[i + 1])))
        weights.append(np.random.uniform(-1, 1, (structure[i], structure[i + 1])))
    return weights, biases

def predict(weights, biases, input):
    a = [None] * len(weights)
    a[0] = input
    for i in range(1, len(weights)):
        a[i] = sigmoid((a[i - 1] @ weights[i]) + biases[i])
    return a[-1]

def calculate_accuracy(weights, biases, data_set):
    total = 0
    for x, y in data_set:
        if np.argmax(y) != np.argmax(predict(weights, biases, x)): 
            total += 1
    return total / len(data_set)

def transform_image(img):
    img = img.reshape(28,28)
    transformations = {
        "up": np.roll(img, -1, axis=0),
        "left": np.roll(img, -1, axis=1),
        "down": np.roll(img, 1, axis=0),
        "right": np.roll(img, 1, axis=1),
        "rotate_right": crop_image(rotate(img, -15)),
        "rotate_left": crop_image(rotate(img, 15)),
        "normal": img
    }
    return transformations[np.random.choice(list(transformations.keys()))].reshape(1, 784)

def crop_image(img):
    y, x = img.shape
    return img[y // 2 - 14 : y // 2 + 14, x // 2 - 14 : x // 2 + 14]

def load_mnist(filename):
    data_set = []
    with open(filename) as file:
        for line in file:
            values = line.strip().split(",")
            data_set.append((
                np.array([[int(i) / 255 for i in values[1:]]]), 
                np.array([int(values[0]) * [0] + [1] + (9 - int(values[0])) * [0]])
            ))
    return data_set

def train_network(weights, biases, train_set, learning_rate=0.1, epochs=100, write=True, distort=False):
    for epoch in range(epochs):
        for x, y in train_set:
            if distort:
                x = transform_image(x)
            a = [x]
            dot = []
            for w, b in zip(weights[1:], biases[1:]): 
                dot.append(a[-1] @ w + b)
                a.append(sigmoid(dot[-1]))
            delta = [sigmoid_prime(dot[-1]) * (y - a[-1])]
            for w, dotL in zip(weights[-1:1:-1], dot[:-1][::-1]):
                delta.append(sigmoid_prime(dotL) * (delta[-1] @ w.T))
            delta.reverse()
            for i in range(1, len(weights)):
                weights[i] += learning_rate * a[i - 1].T @ delta[i - 1]
                biases[i] += learning_rate * delta[i - 1]
        if write:
            with open("weights.pkl", "wb") as f: pickle.dump(weights, f)
            with open("biases.pkl", "wb") as f: pickle.dump(biases, f)
        print(f"Epoch {epoch + 1} completed")

    return weights, biases

structure = [784, 300, 10]
train_set = load_mnist("mnist_train.csv")
test_set = load_mnist("mnist_test.csv")
weights, biases = initialize_network(structure)
weights, biases = train_network(weights, biases, train_set, learning_rate=0.3, epochs=12, distort=True)

print(f"Structure: {structure}")
print(f"Misclassified for training: {calculate_accuracy(weights, biases, train_set) * 100}%")
print(f"Misclassified for testing: {calculate_accuracy(weights, biases, test_set) * 100}%")
print("Number of Epochs: 12")
