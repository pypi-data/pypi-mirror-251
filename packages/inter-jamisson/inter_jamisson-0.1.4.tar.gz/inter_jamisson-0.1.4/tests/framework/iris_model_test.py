from unittest.mock import Mock

import pytest

from inter_jamisson.framework.iris_model import IrisModel
from inter_jamisson.use_cases.base import UseCase


@pytest.fixture
def mock_train_model_usecase():
    return Mock(spec=UseCase)


@pytest.fixture
def mock_evaluate_model_usecase():
    return Mock(spec=UseCase)


@pytest.fixture
def mock_save_model_usecase():
    return Mock(spec=UseCase)


def test_train_model_calls_execute_on_train_model_usecase(
    mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
):
    iris_model = IrisModel(
        mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
    )

    iris_model.train_model()

    mock_train_model_usecase.execute.assert_called_once()


def test_evaluate_model_calls_execute_on_evaluate_model_usecase(
    mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
):
    iris_model = IrisModel(
        mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
    )

    iris_model.evaluate_model()

    mock_evaluate_model_usecase.execute.assert_called_once()


def test_save_model_calls_execute_on_save_model_usecase(
    mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
):
    iris_model = IrisModel(
        mock_train_model_usecase, mock_evaluate_model_usecase, mock_save_model_usecase
    )

    iris_model.save_model()

    mock_save_model_usecase.execute.assert_called_once()


if __name__ == "__main__":
    pytest.main()
