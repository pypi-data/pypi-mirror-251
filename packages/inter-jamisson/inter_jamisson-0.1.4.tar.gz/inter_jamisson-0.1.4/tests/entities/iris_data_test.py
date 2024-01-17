import numpy as np

from inter_jamisson.entities.iris_data import IrisData


def test_attributes():
    X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    X_test = np.array([[10, 11, 12], [13, 14, 15]])
    y_train = np.array([0, 1, 0])
    y_test = np.array([1, 0])

    iris_data = IrisData(X_train, X_test, y_train, y_test)

    np.testing.assert_array_equal(
        iris_data.X_train, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )
    np.testing.assert_array_equal(
        iris_data.X_test, np.array([[10, 11, 12], [13, 14, 15]])
    )
    np.testing.assert_array_equal(iris_data.y_train, np.array([0, 1, 0]))
    np.testing.assert_array_equal(iris_data.y_test, np.array([1, 0]))
