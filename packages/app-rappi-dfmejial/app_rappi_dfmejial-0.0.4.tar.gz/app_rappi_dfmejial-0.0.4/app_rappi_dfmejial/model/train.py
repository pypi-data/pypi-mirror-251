import logging
import os
from pathlib import Path
from typing import Tuple
from joblib import dump, load
import uuid
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

from app_rappi_dfmejial.conf.settings import TRAINING_FEATURES, TRUE_VALUE

logger = logging.getLogger(__name__)

class TitanicModelTrainer:
    """
    A class for training and evaluating a Random Forest classifier on Titanic dataset.

    Attributes:
    - train_ratio (float): The ratio of data to be used for training (default is 0.8).
    - test_ratio (float): The ratio of data to be used for testing (default is 0.2).
    - n_estimators (int): The number of trees in the forest (default is 500).
    - max_depth (int): The maximum depth of the tree (default is 20).

    Methods:
    - __init__: Initializes the TitanicModelTrainer object.
    - split_data: Splits the input data into training and testing sets.
    - train_model: Trains a Random Forest classifier on the training data.
    - evaluate_model: Evaluates the trained model on the testing data.
    - save_model: Saves the trained model to a file.
    - load_model: Loads a trained model from a file.
    """

    def __init__(self, train_ratio: float = 0.8, test_ratio: float = 0.2, n_estimators: int = 500, max_depth: int = 20) -> None:
        """
        Initializes a TitanicModelTrainer instance.

        Parameters:
        - train_ratio (float): The ratio of data to be used for training (default is 0.8).
        - test_ratio (float): The ratio of data to be used for testing (default is 0.2).
        - n_estimators (int): The number of trees in the forest (default is 500).
        - max_depth (int): The maximum depth of the tree (default is 20).
        """
        self.train_ratio = train_ratio
        self.test_ratio = test_ratio
        self.n_estimators = n_estimators
        self.max_depth = max_depth

    def split_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, ...]:
        """
        Splits the input data into training and testing sets.

        Parameters:
        - data (pd.DataFrame): The input data.

        Returns:
        - Tuple[pd.DataFrame]: The tuple containing X_train, X_test, y_train, y_test DataFrames.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            data[TRAINING_FEATURES], data[TRUE_VALUE], test_size=self.test_ratio, random_state=42, stratify=data[TRUE_VALUE])
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
        """
        Trains a Random Forest classifier on the training data.

        Parameters:
        - X_train (pd.DataFrame): The feature matrix for training.
        - y_train (pd.Series): The target variable for training.

        Returns:
        - RandomForestClassifier: The trained Random Forest classifier.
        """
        clf = RandomForestClassifier(
            max_depth=self.max_depth,
            min_samples_leaf=4,
            min_samples_split=2,
            n_estimators=self.n_estimators,
            random_state=42
            )

        logger.warning("Training model!")

        clf.fit(X_train, y_train)

        return clf
    
    @staticmethod
    def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[float, float, float]:
        """
        Evaluates the trained model on the testing data.

        Parameters:
        - model (RandomForestClassifier): The trained Random Forest classifier.
        - X_test (pd.DataFrame): The feature matrix for testing.
        - y_test (pd.Series): The target variable for testing.

        Returns:
        - Tuple[float, float, float]: Precision, Recall, and F1 Score.
        """
        logger.warning("Evaluating model!")

        y_predicted = model.predict(X_test)

        precision = precision_score(y_test, y_predicted)
        recall = recall_score(y_test, y_predicted)
        f1 = f1_score(y_test, y_predicted)

        return precision, recall, f1
    
    @staticmethod
    def save_model(model: RandomForestClassifier) -> str:
        """
        Saves the trained model to a file.

        Parameters:
        - model (RandomForestClassifier): The trained Random Forest classifier.

        Returns:
        - str: The path to the saved model file.
        """
        logger.warning("Saving model!")

        today = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")

        name_uuid = f"{today}_{uuid.uuid4().hex}"

        path = os.path.join(Path.cwd(), f"{name_uuid}.joblib")

        dump(model, path)

        return path
    
    @staticmethod
    def load_model(path: str) -> RandomForestClassifier:
        """
        Loads a trained model from a file.

        Parameters:
        - path (str): The path to the saved model file.

        Returns:
        - RandomForestClassifier: The loaded Random Forest classifier.
        """
        clf = load(path) 

        return clf
    