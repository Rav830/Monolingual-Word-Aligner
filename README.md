# Monolingual-Word-Aligner

This is a clone and update of the Monolingual Word Aligner made by [Rameshjesswani](https://github.com/rameshjesswani/Semantic-Textual-Similarity) The algorithm implemented is from Sultan et. al(2014) [Back to Basics for Monolingual Alignment](http://www.aclweb.org/anthology/Q14-1018)


## Modifications

This aligner has been ported from Python 2 to Python 3 but has only been tested on Python3.7

I only updated the NLTK code to work so using Spacy is currently deprecated.

The code has been sped up by using the Stanford CoreNLP server functionality in NLTK instead of loading in the jar files each time we want to do an alignment.

## Dependencies
Required

* NLTK 3.4.5
* requests 2.22
* Stanford Corenlp-full-2017-06-09

Optional

* xlrd (for the test)

## Installation
* Set up a virtual environment if you want.
* Download the python packages (NLTK and Requests)

