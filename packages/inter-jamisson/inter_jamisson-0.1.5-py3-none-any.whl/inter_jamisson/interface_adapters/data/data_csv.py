import pandas as pd
from sklearn.model_selection import train_test_split

from inter_jamisson.entities.iris_data import IrisData
from inter_jamisson.use_cases.port.data import DataLoader


class DataCSV(DataLoader):
    """Read data from CSV

    Args:
        filename (str): filename to csv file
    """

    def __init__(self, filename: str = None):
        self.filename = filename

    def load_data(self):
        """Read data from CSV

        Returns:
            IrisData: Object with X_train, X_test, y_train, y_test
        """
        iris = pd.read_csv(self.filename, index_col=0)

        y = iris["target"].tolist()
        iris.drop("target", axis="columns", inplace=True)
        X = iris.values.tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return IrisData(X_train, X_test, y_train, y_test)
