from unittest.mock import Mock

import pytest

from inter_jamisson.use_cases.port.model import Model
from inter_jamisson.use_cases.save_model import SaveModel


@pytest.fixture
def mock_model():
    return Mock(spec=Model)


def test_execute_calls_save_method(mock_model):
    file_path = "test.pkl"
    save_model = SaveModel(model=mock_model, file_path=file_path)

    save_model.execute()

    mock_model.save.assert_called_once_with(file_path)


if __name__ == "__main__":
    pytest.main()
