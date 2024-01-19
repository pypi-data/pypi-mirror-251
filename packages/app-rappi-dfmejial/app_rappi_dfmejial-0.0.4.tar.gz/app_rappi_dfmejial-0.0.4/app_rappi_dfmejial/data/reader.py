import os
import logging
from typing import List, Optional
from pathlib import Path

import pandas as pd

from app_rappi_dfmejial.conf.settings import COLS_TO_REMOVE
from app_rappi_dfmejial.data import filepath

logger = logging.getLogger(__name__)

class TitanicDataReader:
    """
    A class for reading and processing Titanic dataset.

    Attributes:
    - cols_to_remove (Optional[List[str]]): A list of column names to be removed from the dataset.
    - data_path (str): The path to the directory containing the raw data files.

    Methods:
    - __init__: Initializes the TitanicDataReader object.
    - read_raw_data: Reads the raw data from a specified data split (default is "train").
    - remove_cols: Removes specified columns from the raw data.
    """

    def __init__(
            self,
            cols_to_remove: Optional[List[str]] = None,
            data_path: Optional[str] = None
            ) -> None:
        """
        Initializes a TitanicDataReader instance.

        Parameters:
        - cols_to_remove (Optional[List[str]]): A list of column names to be removed.
        - data_path (Optional[str]): The path to the directory containing raw data.
        """
        if data_path:
            self.data_path = data_path
        else:
            self.data_path = filepath

        self.cols_to_remove = COLS_TO_REMOVE if cols_to_remove is None else cols_to_remove

    def read_raw_data(self, data_split: str = "train") -> pd.DataFrame:
        """
        Reads raw data from the specified data split.

        Parameters:
        - data_split (str): The data split to read (default is "train").

        Returns:
        - pd.DataFrame: The raw data.
        """
        data_split_path = os.path.join(self.data_path, f"{data_split}.csv")
        raw_data = pd.read_csv(data_split_path)

        logger.warning("Read %s data split with %s rows!", data_split, len(raw_data))

        return raw_data

    def remove_cols(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Removes specified columns from the raw data.

        Parameters:
        - raw_data (pd.DataFrame): The raw data.

        Returns:
        - pd.DataFrame: The raw data with specified columns removed.
        """
        raw_data = raw_data.drop(columns=self.cols_to_remove)
        
        logger.warning("Removed columns: %s", self.cols_to_remove)

        return raw_data
