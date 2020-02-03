#!/bin/bash

java -mx4g -cp "./CoreNLP_Setup/stanford-corenlp-full-2017-06-09/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,depparse -port 9000 -timeout 150000 2>&1|tee serverLog.txt
