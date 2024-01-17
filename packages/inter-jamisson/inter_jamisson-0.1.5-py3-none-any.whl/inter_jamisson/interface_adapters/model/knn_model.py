import pickle

from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier

from inter_jamisson.use_cases.port.model import Model


class KNNModel(Model):
    """KNNModel implementation

    Args:
        filename (str) [optional]: filename model .pkl
    """

    def __init__(self, filename: str = None):
        if filename:
            with open(filename, "rb") as file:
                self.model = pickle.load(file)
        else:
            self.model = KNeighborsClassifier()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Acurácia do modelo: {accuracy:.2f}")
        print("Relatório de Classificação:")
        print(classification_report(y_test, predictions))

    def save(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self.model, file)
