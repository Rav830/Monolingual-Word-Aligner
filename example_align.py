from wordAligner import *
import sys

sentence1 = "I ate an apple"
sentence2 = "I ate an pear"

print("sentence1 = ", sentence1)
print("sentence2 = ", sentence2)



if __name__ == '__main__':

    flag = sys.argv[1]

    processing = Aligner(flag)
    processing.align_sentences(sentence1,sentence2)
