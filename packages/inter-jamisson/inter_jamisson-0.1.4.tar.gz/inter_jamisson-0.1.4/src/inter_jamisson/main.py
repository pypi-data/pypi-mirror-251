from inter_jamisson.framework.iris_model import IrisModel
from inter_jamisson.interface_adapters.data.data_sklearn import DataSklearn
from inter_jamisson.interface_adapters.model.knn_model import KNNModel
from inter_jamisson.use_cases.evaluate_model import EvaluateModel
from inter_jamisson.use_cases.save_model import SaveModel
from inter_jamisson.use_cases.train_model import TrainModel

if __name__ == "__main__":
    data_loader = DataSklearn()
    knn_model = KNNModel()

    iris_data = data_loader.load_data()

    train_model_usecase = TrainModel(knn_model, iris_data)
    evaluate_model_usecase = EvaluateModel(knn_model, iris_data)
    save_model_usercase = SaveModel(knn_model, "ola.pkl")

    final_model = IrisModel(
        train_model_usecase, evaluate_model_usecase, save_model_usercase
    )

    final_model.train_model()
    final_model.evaluate_model()
    final_model.save_model()
