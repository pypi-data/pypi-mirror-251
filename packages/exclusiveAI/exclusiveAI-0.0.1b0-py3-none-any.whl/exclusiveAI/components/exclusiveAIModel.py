import pickle

import numpy as np
from exclusiveAI.components.Optimizers import Optimizer
from exclusiveAI.components.Metrics import MetricUtils
from exclusiveAI import utils
from tqdm import tqdm


class exclusiveAIModel:
    """
    This class is used to create a neural network model.

    Args:

        layers (list): A list of layers to be added to the model.
        optimizer (Optimizer): The optimizer to be used for training.
        callbacks (list): A list of callbacks to be used during training.
        metrics (list): A list of metrics to be used during training.
        verbose (bool): Whether to print out the progress of the model.
        shuffle (bool): Whether to shuffle the data before training.
    Attributes:

        optimizer (Optimizer): The optimizer to be used for training.
        callbacks (list): A list of callbacks to be used during training.
        layers (list): A list of layers to be added to the model.
        verbose (bool): Whether to print out the progress of the model.
        early_stop (bool): Whether to use early stopping as stopping criteria.
        name (str): The name of the model.
        curr_epoch (int): The current epoch of the model.
        metrics (list): A list of metrics to be used during training.
        history (dict): A dictionary containing the training history metrics.
    """

    def __init__(self,
                 layers: list,
                 optimizer: Optimizer,
                 callbacks: list,
                 metrics: [],
                 verbose: bool = False,
                 shuffle: bool = True
                 ):
        self.optimizer = optimizer
        self.callbacks = callbacks
        self.layers = layers
        self.verbose = verbose
        self.early_stop = False
        self.name = 'Model ' + str(len(self.layers))
        self.curr_epoch = 0
        self.metrics = metrics
        self.history = {}
        self.shuffle = shuffle

        self.best_loss = float('inf')
        self.best_weights = None
        self.best_epoch = 0
        self.patience = 0

        self.initialize()

    def initialize(self):
        """
        Initialize the layers of the model
        """
        self.layers[0].initialize(name='Input', verbose=self.verbose)
        for i, layer in enumerate(self.layers[1:]):
            layer.initialize(self.layers[i], name=('Layer' + str(i)), verbose=self.verbose)

    def train(self, *args):
        pass


    def get_last(self, index=-1):
        """
        Get the last element of the history.
        Returns: the last element of the history.
        """

        return {name: self.history[name][index] for name in self.history}

    def predict(self, input: np.array):
        """
        Apply the feedforward across layers to the input data.
        Args:
            input:

        Returns:

        """
        input = input
        output = None
        for layer in self.layers:
            output = layer.feedforward(input)
            input = output
        return output

    def evaluate(self, input: np.array, input_label: np.array, metrics=None):
        """
        Apply the predict and calculate the metrics on prediction.
        Args:
            input: input data
            input_label: input label
            metrics: metrics to calculate

        Returns: metrics on prediction
        """
        if metrics is None:
            metrics = ['mse', 'binary_accuracy']
        output = self.predict(input)
        return [MetricUtils.calculate(metric, target=input_label, predicted=output) for metric in metrics]

    def get_weights(self):
        weights = []
        for layer in self.layers:
            weights.append(layer.get_weights())
        return weights

    def set_weights(self, weights: list):
        for layer, weight in zip(self.layers, weights):
            layer.set_weights(weight)

    def save(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename: str):
        with open(filename, 'rb') as f:
            return pickle.load(f)