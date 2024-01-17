class IrisData:
    """
    A class to encapsulate Iris dataset attributes.

    This class stores the training and testing data for the Iris dataset,
    making it convenient to access and manipulate the data for machine learning tasks.

    Attributes:
        X_train (numpy.ndarray): The training features.
        X_test (numpy.ndarray): The testing features.
        y_train (numpy.ndarray): The training labels.
        y_test (numpy.ndarray): The testing labels.
    """

    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
