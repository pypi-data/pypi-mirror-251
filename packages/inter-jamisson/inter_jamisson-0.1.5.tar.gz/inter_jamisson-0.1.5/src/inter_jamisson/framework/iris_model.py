from inter_jamisson.use_cases.base import UseCase


class IrisModel:
    """Framework to execute usercases to IrisModel"""

    def __init__(
        self,
        train_model_usecase: UseCase,
        evaluate_model_usecase: UseCase,
        save_model_usecase: UseCase,
    ):
        self.train_model_usecase = train_model_usecase
        self.evaluate_model_usecase = evaluate_model_usecase
        self.save_model_usecase = save_model_usecase

    def train_model(self):
        """Train model execution"""
        self.train_model_usecase.execute()

    def evaluate_model(self):
        """evaluate model execution"""
        self.evaluate_model_usecase.execute()

    def save_model(self):
        """save model execution"""
        self.save_model_usecase.execute()
