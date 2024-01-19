import logging
import argparse

from app_rappi_dfmejial.data.reader import TitanicDataReader
from app_rappi_dfmejial.data.pre_processer import TitanicDataPreprocessor
from app_rappi_dfmejial.model.train import TitanicModelTrainer

logger = logging.getLogger(__name__)

class RappiChallenge:
    """
    A class representing the Rappi Challenge workflow.

    Methods:
    - run_challenge: Executes the Rappi Challenge workflow, including data reading, preprocessing, model training, and evaluation.
    """

    def __init__(self, n_estimators: int, max_depth: int, save_model: bool = False) -> None:
        
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.save_model = save_model

    def run_challenge(self) -> str:
        """
        Executes the Rappi Challenge workflow.

        Returns:
        - str: The path to the saved trained model.
        """

        # Step 1: Read and preprocess data
        reader = TitanicDataReader()
        raw_data = reader.read_raw_data()
        raw_data = reader.remove_cols(raw_data)

        # Step 2: Split data and preprocess
        trainer = TitanicModelTrainer(n_estimators=self.n_estimators, max_depth=self.max_depth)
        X_train, X_test, y_train, y_test = trainer.split_data(raw_data)

        pre_processor = TitanicDataPreprocessor()
        X_train = pre_processor.apply_preprocessing(X_train)
        X_test = pre_processor.apply_preprocessing(X_test)

        # Step 3: Train and evaluate the model
        clf = trainer.train_model(X_train, y_train)
        precision, recall, f1 = trainer.evaluate_model(clf, X_test, y_test)

        logger.warning("Precision on test set: %s", precision)
        logger.warning("Recall on test set: %s", recall)
        logger.warning("F1 on test set: %s", f1)

        # Step 4: Save the trained model
        if self.save_model:
            path = trainer.save_model(clf)
            logger.warning("Model saved on %s", path)
            
            return path
    

def main() -> None:
    """
    Runs the Rappi Challenge.
    """
    parser = argparse.ArgumentParser(description="Basic CLI")
    parser.add_argument("--estimators", dest="estimators", type=int, help="Number of trees to use in training.", default=500)
    parser.add_argument("--depth", dest="depth", type=int, default=20, help="Max depth of each tree")
    parser.add_argument("--save-model", dest="save", help="Whether to sotre trained model", default=False, action="store_true")
    args = parser.parse_args()

    rappi_challenge = RappiChallenge(n_estimators=args.estimators, max_depth=args.depth, save_model=args.save)
    rappi_challenge.run_challenge()

if __name__ == "__main__":
    main()
