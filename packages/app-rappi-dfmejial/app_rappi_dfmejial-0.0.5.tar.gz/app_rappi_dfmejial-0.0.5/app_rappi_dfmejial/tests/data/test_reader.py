import pandas as pd
import pytest
from app_rappi_dfmejial.data.reader import TitanicDataReader

@pytest.fixture
def titanic_data_reader():
    return TitanicDataReader()

def test_read_raw_data(titanic_data_reader):
    data_split = "train"
    raw_data = titanic_data_reader.read_raw_data(data_split)
    assert isinstance(raw_data, pd.DataFrame)
    assert len(raw_data) > 0

def test_remove_cols(titanic_data_reader):
    data_split = "train"
    raw_data = titanic_data_reader.read_raw_data(data_split)
    modified_data = titanic_data_reader.remove_cols(raw_data)
    assert isinstance(modified_data, pd.DataFrame)
    assert "PassengerId" not in modified_data.columns