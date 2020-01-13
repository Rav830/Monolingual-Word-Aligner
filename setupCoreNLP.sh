#!/bin/sh

echo "Downloading Stanford CoreNLP Full 2017-06-09" &&\
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip -O ./CoreNLP_Setup/stanford-corenlp-full-2017-06-09.zip &&\
echo "unzipping the download" &&\
unzip ./CoreNLP_Setup/stanford-corenlp-full-2017-06-09.zip -d ./CoreNLP_Setup &&\
echo "done";

