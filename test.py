"""Evaluate the saved spam classifier on data/testing_spam.csv."""

import pickle
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
TEST_FILE = ROOT / "data" / "testing_spam.csv"
MODEL_FILE = ROOT / "spam_classifier_model.pkl"


def main():
    with MODEL_FILE.open("rb") as model_file:
        classifier = pickle.load(model_file)

    testing_data = np.loadtxt(TEST_FILE, delimiter=",").astype(int)
    test_labels = testing_data[:, 0]
    test_features = testing_data[:, 1:]
    predictions = classifier.predict(test_features)
    accuracy = np.mean(predictions == test_labels)
    print(f"Test accuracy: {accuracy:.2%} ({(predictions == test_labels).sum()}/{len(test_labels)})")


if __name__ == "__main__":
    main()
