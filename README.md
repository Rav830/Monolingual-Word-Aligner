# Monolingual-Word-Aligner

This is a clone and update of the Monolingual Word Aligner that [Rameshjesswani](https://github.com/rameshjesswani/Semantic-Textual-Similarity) converted to use NLTK. The algorithm implemented is from Sultan et. al(2014) [Back to Basics for Monolingual Alignment](http://www.aclweb.org/anthology/Q14-1018)


## Modifications

This aligner has been ported from Python 2 to Python 3 but has only been tested on Python3.7

I only updated the NLTK code to work so using Spacy is currently deprecated.

The code has been sped up by using the Stanford CoreNLP server functionality in NLTK instead of loading in the jar files each time we want to do an alignment.

## Dependencies
Required

* NLTK 3.4.5
* requests 2.22
* Stanford CoreNLP full 2017-06-09
  * CoreNLP also depends on Java 8

Optional

* xlrd (for the test)

## Installation
* Set up a virtual environment if you want.
* Download the python packages (NLTK and Requests)
* Make sure Java 8 is installed and being used
* run the `setupCoreNLP.sh` file to download and unzip the the stanford corenlp server
  * Note: it uses wget and unzip so make sure those programs are available



## Usage

Start the Stanford NLP server

```bash
java -mx4g -cp "./CoreNLP_Setup/stanford-corenlp-full-2017-06-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,depparse -port 9000 -timeout 15000
```

Then you can run `example_align.py` to test to see if it is working.

## Note:

I am assuming that the server is being hosted on localhost port 9000. If you need to change this, nltkUtil.py should be modified to pull it off.

Also for some reason the paraphrase database that is used has some unique pairs that are odd, such as \x16 paired with \x1d and \x1e is paired with 'i'. These are ignored and just printed out that we "Failed on" because the program couldn't parse those symbols\

## Potential Issues 

The tokenization uses both NLTK's and Stanford's Tokenizer. This can cause token mismatches with one token example being "<text\>". NLTK will split that into "<" "text" ">" but Stanford will keep it together.