from inter_jamisson.use_cases.base import UseCase


class SaveModel(UseCase):
    def __init__(self, model, file_path):
        self.model = model
        self.file_path = file_path

    def execute(self):
        self.model.save(self.file_path)
