# Glossary

Use this page to record terms and ideas that help you understand
professional analytics projects.

This project covers classification: building and evaluating models
that predict a category from input features.

Pro-tip: Expand the VS Code **Outline** view (below the navigator on the right)
to see this file organization at-a-glance.

## Training and Evaluation

### training set

The training set is the portion of data used to fit the model.
The model sees these examples and adjusts its internal parameters to minimize error.

### test set

The test set is the portion of data held back from training
and used only to evaluate the model on unseen examples.
A good test score suggests the model generalizes beyond the training data.

### train-test split

A train-test split divides the dataset into a training portion and a test portion.
A common split is 80% training and 20% test.

### overfitting

Overfitting happens when a model learns the training data too closely
and performs poorly on new, unseen data.
A large gap between training accuracy and test accuracy is a sign of overfitting.

### accuracy

Accuracy is the fraction of predictions that are correct.
It is a useful metric when classes are roughly balanced
but can be misleading when one class is much more common than others.

### confusion matrix

A confusion matrix shows how often a classifier predicted each class
compared to the true class.
Each row represents the true class; each column represents the predicted class.
Off-diagonal entries are misclassifications.

### precision

Precision is the fraction of positive predictions that were actually correct.
High precision means the model rarely predicts a class when it should not.

### recall

Recall is the fraction of actual positives that the model correctly identified.
High recall means the model rarely misses a true positive.

### F1 score

The F1 score is the harmonic mean of precision and recall.
It balances both concerns and is useful when false positives and false negatives
both carry real cost.

### classification report

A classification report shows precision, recall, and F1 score
for each class in the target.
It gives a fuller picture of model performance than accuracy alone.

## Classification Models

### decision tree

A decision tree is a classifier that makes predictions by asking a sequence
of yes/no questions about feature values.
It is easy to interpret but can overfit if grown too deep.

### logistic regression

Logistic regression is a linear classifier that estimates the probability
that an input belongs to each class.
Despite the name, it is a classification model, not a regression model.

### k-nearest neighbors (k-NN)

k-NN is a classifier that predicts the class of a new point
by finding the k most similar training examples and taking a majority vote.
It is simple but can be slow on large datasets.
