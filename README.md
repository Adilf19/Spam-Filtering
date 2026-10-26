# Spam filtering with Bernoulli Naive Bayes

This is a standalone version of my university coursework implementation. I moved the classifier out of the notebook so the training and testing steps are easier to run; the notebook itself is not included.

The model uses 54 binary email features. It estimates the spam and ham probabilities with additive smoothing (`k = 0.1`), then predicts the class with the higher log probability.

## Run it

Install NumPy, then run:

```bash
python -m pip install -r requirements.txt
python train.py
python test.py
```

`train.py` fits the model using `data/training_spam.csv` and saves it as `spam_classifier_model.pkl`. `test.py` loads that model and evaluates it using `data/testing_spam.csv`. Each CSV row starts with its label (`1` for spam and `0` for ham), followed by the 54 features. The training file has 1,000 rows; the test file has 500.

## Result

The classifier got **445 of 500 emails right (89%)** on the supplied test set. My notebook's accuracy estimate was also 89%.

`AI_video.py` and `spam-classifier-demo.MOV` are included with the project files.
