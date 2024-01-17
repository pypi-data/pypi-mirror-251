from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from inter_jamisson.entities.iris_data import IrisData
from inter_jamisson.use_cases.port.data import DataLoader


class DataSklearn(DataLoader):
    """Read data from load_iris sklearn"""

    def load_data(self):
        """Read data from load_iris sklearn

        Returns:
            IrisData: Object with X_train, X_test, y_train, y_test
        """

        iris = load_iris()
        X = iris.data
        y = iris.target

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.5, random_state=42
        )
        return IrisData(X_train, X_test, y_train, y_test)
