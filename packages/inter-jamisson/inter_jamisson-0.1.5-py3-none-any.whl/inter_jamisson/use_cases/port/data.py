from abc import ABC, abstractmethod


class DataLoader(ABC):
    @abstractmethod
    def load_data(self):
        """Read data from file

        Returns:
            IrisData: Object with X_train, X_test, y_train, y_test
        """
        pass
