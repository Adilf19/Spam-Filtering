"""Train the spam classifier on data/training_spam.csv and save the model."""

import pickle
from pathlib import Path

import numpy as np

from spam_classifier import create_classifier

ROOT = Path(__file__).resolve().parent
TRAINING_FILE = ROOT / "data" / "training_spam.csv"
MODEL_FILE = ROOT / "spam_classifier_model.pkl"


def main():
    training_data = np.loadtxt(TRAINING_FILE, delimiter=",").astype(int)
    classifier = create_classifier(training_data, k=0.1)
    with MODEL_FILE.open("wb") as model_file:
        pickle.dump(classifier, model_file)
    print(f"Trained on {len(training_data)} examples; saved model to {MODEL_FILE.name}.")


if __name__ == "__main__":
    main()
