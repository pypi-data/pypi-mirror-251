from unittest.mock import Mock

import numpy as np
import pytest

from inter_jamisson.entities.iris_data import IrisData
from inter_jamisson.use_cases.evaluate_model import EvaluateModel
from inter_jamisson.use_cases.port.model import Model


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


def test_execute_calls_evaluate_method(mock_model, mock_data):
    evaluate_model = EvaluateModel(model=mock_model, data=mock_data)

    evaluate_model.execute()

    mock_model.evaluate.assert_called_once_with(mock_data.X_test, mock_data.y_test)


if __name__ == "__main__":
    pytest.main()
