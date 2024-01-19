from typing import Dict, Optional, Union
import pandas as pd

class TitanicDataPreprocessor:
    """
    A class for preprocessing Titanic dataset features.

    Attributes:
    - sex_lookup (Dict): A dictionary for encoding the 'Sex' feature.
    - deck_lookup (Dict): A dictionary for encoding the 'Embarked' feature.
    - age_median (Optional[float]): The median age for filling missing values in the 'Age' feature.
    - most_common_deck (str): The most common deck for filling missing values in the 'Embarked' feature.
    - fare_mean (Optional[float]): The mean fare for standard scaling the 'Fare' feature.
    - fare_std (Optional[float]): The standard deviation of fare for standard scaling the 'Fare' feature.

    Methods:
    - __init__: Initializes the TitanicDataPreprocessor object.
    - apply_preprocessing: Applies preprocessing steps to the input data.
    - encode_feature: Encodes a categorical feature using a lookup dictionary.
    - fill_na_data: Fills missing values in a specified column with a default value.
    - apply_standard_scaling: Applies standard scaling to a numerical feature.
    """

    def __init__(self) -> None:
        """
        Initializes a TitanicDataPreprocessor instance with default values.
        """
        self.sex_lookup = {"male": 0, "female": 1}
        self.deck_lookup = {"S": 0, "C": 1, "Q": 2}
        self.age_median = None
        self.most_common_deck = "S"
        self.fare_mean = None
        self.fare_std = None

    def apply_preprocessing(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Applies preprocessing steps to the input data.

        Parameters:
        - data (pd.DataFrame): The input data.

        Returns:
        - pd.DataFrame: The preprocessed data.
        """
        data = self.encode_feature(data, "Sex", self.sex_lookup, 2)

        self.age_median = data.Age.median() if self.age_median is None else self.age_median
        data = self.fill_na_data(data, "Age", self.age_median)

        self.fare_mean = data.Fare.mean() if self.fare_mean is None else self.fare_mean
        self.fare_std = data.Fare.std() if self.fare_std is None else self.fare_std
        data = self.apply_standard_scaling(data, "Fare", self.fare_mean, self.fare_std)

        data = self.fill_na_data(data, "Embarked", self.most_common_deck)
        data = self.encode_feature(data, "Embarked", self.deck_lookup, 3)

        return data

    @staticmethod
    def encode_feature(data: pd.DataFrame, column: str, lookup: Dict, default_value: Optional[Union[str, int]] = None) -> pd.DataFrame:
        """
        Encodes a categorical feature in the DataFrame using a lookup dictionary.

        Parameters:
        - data (pd.DataFrame): The input data.
        - column (str): The column to be encoded.
        - lookup (Dict): A dictionary for encoding the feature.
        - default_value (Optional[Union[str, int]]): Default value if the feature value is not found in the lookup.

        Returns:
        - pd.DataFrame: The DataFrame with the encoded feature.
        """
        data[column] = data[column].apply(lambda x: lookup.get(x, default_value))

        return data

    @staticmethod
    def fill_na_data(data: pd.DataFrame, column: str, default_value: Optional[Union[str, int]] = None) -> pd.DataFrame:
        """
        Fills missing values in a specified column with a default value.

        Parameters:
        - data (pd.DataFrame): The input data.
        - column (str): The column with missing values to be filled.
        - default_value (Optional[Union[str, int]]): Default value for filling missing values.

        Returns:
        - pd.DataFrame: The DataFrame with missing values filled.
        """

        data[column] = data[column].fillna(value=default_value)

        return data

    @staticmethod
    def apply_standard_scaling(data: pd.DataFrame, column: str, mean: float, std: float) -> pd.DataFrame:
        """
        Applies standard scaling to a numerical feature in the DataFrame.

        Parameters:
        - data (pd.DataFrame): The input data.
        - column (str): The numerical column to be scaled.
        - mean (float): The mean for standard scaling.
        - std (float): The standard deviation for standard scaling.

        Returns:
        - pd.DataFrame: The DataFrame with the scaled feature.
        """

        data[column] = (data[column] - mean) / std
        
        return data
