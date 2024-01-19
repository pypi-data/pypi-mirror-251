import pandas as pd
import pytest
from app_rappi_dfmejial.data.pre_processer import TitanicDataPreprocessor

@pytest.fixture
def titanic_data_preprocessor():
    return TitanicDataPreprocessor()

def test_apply_preprocessing(titanic_data_preprocessor):
    raw_data = pd.DataFrame({"Sex": ["male", "female"], "Age": [25, None], "Fare": [50.0, 30.0], "Embarked": ["S", "C"]})
    preprocessed_data = titanic_data_preprocessor.apply_preprocessing(raw_data)
    assert isinstance(preprocessed_data, pd.DataFrame)
    assert set(list(preprocessed_data.Sex.unique())).issubset(set([0, 1]))

def test_encode_feature(titanic_data_preprocessor):
    data = pd.DataFrame({"Column": ["value1", "value2"]})
    encoded_data = titanic_data_preprocessor.encode_feature(data, "Column", {"value1": 0, "value2": 1})
    assert isinstance(encoded_data, pd.DataFrame)
    assert set(list(encoded_data.Column.unique())).issubset(set([0, 1]))