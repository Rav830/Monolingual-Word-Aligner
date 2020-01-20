from wordAligner import *
import sys

sentence1 = "I ate an apple. I drove a car."
sentence2 = "I ate an pear"

print("sentence1 = ", sentence1)
print("sentence2 = ", sentence2)



if __name__ == '__main__':

    flag = sys.argv[1]

    processing = Aligner(flag)
    
    for x in range(5):
        processing.align_sentences(sentence1,sentence2)
    
    #from dataBuffer import *
    #dumpStore()
