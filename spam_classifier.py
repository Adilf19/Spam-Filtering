"""Bernoulli Naive Bayes spam classifier from the coursework notebook."""

import numpy as np


class SpamClassifier:
    """Binary Bernoulli Naive Bayes model for 54 binary email features."""

    def __init__(self, k=0.1):
        self.k = k

    def train(self, data):
        labels = data[:, 0]
        features = data[:, 1:]

        spam_emails = features[labels == 1]
        ham_emails = features[labels == 0]
        total = len(labels)

        self.log_prior_spam = np.log(len(spam_emails) / total)
        self.log_prior_ham = np.log(len(ham_emails) / total)

        self.log_likelihood_spam = np.log(
            (spam_emails.sum(axis=0) + self.k)
            / (len(spam_emails) + 2 * self.k)
        )
        self.log_likelihood_ham = np.log(
            (ham_emails.sum(axis=0) + self.k)
            / (len(ham_emails) + 2 * self.k)
        )

        self.log_likelihood_spam_0 = np.log(1 - np.exp(self.log_likelihood_spam))
        self.log_likelihood_ham_0 = np.log(1 - np.exp(self.log_likelihood_ham))
        return self

    def predict(self, data):
        data = np.asarray(data)
        log_prob_spam = (
            self.log_prior_spam
            + (data * self.log_likelihood_spam).sum(axis=1)
            + ((1 - data) * self.log_likelihood_spam_0).sum(axis=1)
        )
        log_prob_ham = (
            self.log_prior_ham
            + (data * self.log_likelihood_ham).sum(axis=1)
            + ((1 - data) * self.log_likelihood_ham_0).sum(axis=1)
        )
        return (log_prob_spam > log_prob_ham).astype(int)


def create_classifier(training_data, k=0.1):
    """Fit and return the classifier from a full CSV matrix (label + features)."""
    return SpamClassifier(k=k).train(np.asarray(training_data))
