import pickle

import numpy as np
from exclusiveAI.components.Optimizers import Optimizer
from exclusiveAI.components.Metrics import MetricUtils
from .exclusiveAIModel import exclusiveAIModel
from exclusiveAI import utils
from tqdm import tqdm


class NeuralNetwork(exclusiveAIModel):
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
        super().__init__(layers, optimizer, callbacks, metrics, verbose, shuffle)

    def train(self,
              inputs: np.array,
              input_label: np.array,
              val: np.array = None,
              val_labels: np.array = None,
              epochs=100, batch_size=32, name: str = '', disable_line=False):
        """
        Perform the model training on input data and label.

        Args:
            inputs (np.array): the input data
            input_label (np.array) the label data
            val (np.array): the validation data
            val_labels (no.array): the validation data label
            epochs (int): the number of epochs
            batch_size (int): the size of a batch used in minibatch approach
            disable_line (bool): show line
            name: name of the model

        Returns: training history

        """

        # cast array to float64
        # check if both val and val_label are provided
        if val is not None and val_labels is not None:
            # check if val and val_label have the same shape
            if val.shape[0] != val_labels.shape[0]:
                raise ValueError("val and val_label must have the same shape")
        MetricUtils.initialize_history(self, val is not None)
        for callback in self.callbacks:
            callback.reset()
        with tqdm(total=epochs, desc="Epochs", colour="white", disable=disable_line) as pbar:
            for epoch in range(epochs):
                output = self.predict(inputs)

                val_output = None
                if val is not None:
                    val_output = self.predict(val)

                MetricUtils.add_to_history(self, output, input_label, val_output, val_labels)
                for callback in self.callbacks:
                    callback(self)

                if self.early_stop:
                    [callback.close() for callback in self.callbacks]
                    break

                self.curr_epoch += 1

                if self.shuffle:
                    perm = np.random.permutation(inputs.shape[0])
                    inputs = np.take(inputs, perm, axis=0)
                    input_label = np.take(input_label, perm, axis=0)
                batches = utils.split_batches(inputs, input_label, batch_size)
                for (batch, batch_label) in batches:
                    self.optimizer.update(self, batch, batch_label)
                pbar.update(1)
                if name != '':
                    pbar.set_description(name)
                pbar.set_postfix(self.get_last())

            pbar.close()
        return self.history