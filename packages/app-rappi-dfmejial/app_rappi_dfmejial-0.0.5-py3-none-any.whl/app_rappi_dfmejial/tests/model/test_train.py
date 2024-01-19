import pandas as pd
import pytest
from app_rappi_dfmejial.model.train import TitanicModelTrainer
from app_rappi_dfmejial.data.reader import TitanicDataReader
from sklearn.ensemble import RandomForestClassifier

@pytest.fixture
def titanic_model_trainer():
    return TitanicModelTrainer()

@pytest.fixture
def titanic_data_reader():
    return TitanicDataReader()

def test_split_data(titanic_model_trainer, titanic_data_reader):
    data_split = "train"
    raw_data = titanic_data_reader.read_raw_data(data_split)
    X_train, X_test, y_train, y_test = titanic_model_trainer.split_data(raw_data)
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

def test_train_model(titanic_model_trainer):
    X_train = pd.DataFrame({"Feature1": [1, 2, 3], "Feature2": [1, 2, 2]})
    y_train = pd.Series([0, 1, 0])
    model = titanic_model_trainer.train_model(X_train, y_train)
    assert isinstance(model, RandomForestClassifier)