from inter_jamisson.use_cases.base import UseCase


class TrainModel(UseCase):
    def __init__(self, model, data):
        self.model = model
        self.data = data

    def execute(self):
        self.model.train(self.data.X_train, self.data.y_train)
