#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 09:47:41 2017

@author: raudi candra
"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction import DictVectorizer
import numpy

X = []
y = []
f = open('en-ud-train.conllu', 'r')
for line in f:
  sentence = line.split("\t")
  if sentence[0].isdigit():
    X.append( {
      'word': sentence[1],
      'is_first': sentence[0] == '1',
      'is_last': sentence[0] == len(sentence) - 1,
      'is_capitalized': sentence[1][0].upper() == sentence[1][0],
      'is_all_caps': sentence[1].upper() == sentence[1],
      'is_all_lower': sentence[1].lower() == sentence[1],
      'prefix-1': sentence[1][0],
      'prefix-2': sentence[1][:2],
      'prefix-3': sentence[1][:3],
      'suffix-1': sentence[1][-1],
      'suffix-2': sentence[1][-2:],
      'suffix-3': sentence[1][-3:],
      'prev_tag': '' if sentence[0] == '1' else y[len(X)-1],
      'prev_word': '' if sentence[0] == '1' else X[len(X)-1]['word'],
      'has_hyphen': '-' in sentence[1],
      'is_numeric': sentence[1].isdigit(),
      'capitals_inside': sentence[1][1:].lower() != sentence[1][1:] }
    )
    y.append(sentence[4])
f.close

print "Feature data size : "+str(len(X))
print "Label data size : "+str(len(y))

v = DictVectorizer(sparse=False)
X = v.fit_transform(X)
v = None

print "Dividing dataset into training set and testing set ..."
cutoff = int(.75 * len(X))
training_sentences = X[:cutoff]
training_tags = y[:cutoff]
test_sentences = X[cutoff:]
test_tags = y[cutoff:]
X = []
y = []

print "Training set size : "+str(len(training_sentences))  
print "Testing set size : "+str(len(test_sentences))


clf = SGDClassifier(loss='log')
#clf = svm.SVC(decision_function_shape='ovo')
#clf = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)

print 'Training started'
n_iter = 12
for n in range(n_iter):
    clf.partial_fit(training_sentences[(n*10000):((n+1)*10000)], training_tags[(n*10000):((n+1)*10000)],classes=numpy.unique(training_tags))  
    print "Training progress "+str((n*10000))
print 'Training completed'
 
print "Testing started"
score = clf.score(test_sentences, test_tags)
print "Accuracy:", score
