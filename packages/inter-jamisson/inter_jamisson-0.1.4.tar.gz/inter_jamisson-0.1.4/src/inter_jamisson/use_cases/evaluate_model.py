from inter_jamisson.use_cases.base import UseCase


class EvaluateModel(UseCase):
    def __init__(self, model, data):
        self.model = model
        self.data = data

    def execute(self):
        self.model.evaluate(self.data.X_test, self.data.y_test)
