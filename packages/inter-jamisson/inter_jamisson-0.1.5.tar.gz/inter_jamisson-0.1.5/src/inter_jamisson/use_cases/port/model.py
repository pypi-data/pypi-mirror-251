from abc import ABC, abstractmethod

from numpy import ndarray


class Model(ABC):
    @abstractmethod
    def train(self, X_train: ndarray, y_train: ndarray):
        """implementation for training

        Args:
            X_train (ndarray): The training features.
            y_train (ndarray): The training labels.
        """
        pass

    @abstractmethod
    def evaluate(self, X_test: ndarray, y_test: ndarray):
        """implementation for evaluate

        Args:
            X_test (ndarray): The test features.
            y_test (ndarray): The test labels.
        """
        pass

    @abstractmethod
    def save(self, file_path: str):
        """implementation for save

        Args:
            file_path (str): path to save file
        """
        pass
