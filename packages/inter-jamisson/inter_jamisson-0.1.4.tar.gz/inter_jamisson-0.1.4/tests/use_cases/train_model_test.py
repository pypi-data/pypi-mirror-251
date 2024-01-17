from unittest.mock import Mock

import numpy as np
import pytest

from inter_jamisson.entities.iris_data import IrisData
from inter_jamisson.use_cases.port.model import Model
from inter_jamisson.use_cases.train_model import TrainModel


@pytest.fixture
def mock_model():
    return Mock(spec=Model)


@pytest.fixture
def mock_data():
    mock_iris_data = Mock(spec=IrisData)

    mock_iris_data.X_train = np.random.rand(2, 3).tolist()
    mock_iris_data.X_test = np.random.rand(2, 3).tolist()
    mock_iris_data.y_train = np.random.randint(0, 2, size=2).tolist()
    mock_iris_data.y_test = np.random.randint(2, 4, size=2).tolist()

    return mock_iris_data


def test_execute_calls_train_method(mock_model, mock_data):
    train_model = TrainModel(model=mock_model, data=mock_data)

    train_model.execute()

    mock_model.train.assert_called_once_with(mock_data.X_train, mock_data.y_train)


if __name__ == "__main__":
    pytest.main()
