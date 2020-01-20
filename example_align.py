from wordAligner import *
import sys

sentence1 = "I ate an apple. I drove a car."
sentence2 = "I ate an pear"

large1 = "I um I don't know if I would stay a fireman. Because even if society sees burning books as okay I don't know how mor-, I don't know how people morally feel about burning other people by accident? So I don't really know what I would do."
large2 = "To advance St 1's claim. Uh you have to think of it as, well I'm not saying you have to think of it as like Montag situation. But if it was as Montag, I feel like he would have more of a uh hesitant approach to it because he actually reads books and he owns books. So he would agree more with the, more with the woman than the fireman."

print("sentence1 = ", sentence1)
print("sentence2 = ", sentence2)



if __name__ == '__main__':

    flag = sys.argv[1]

    processing = Aligner(flag)
    
    
    print("\nSet to Slow\n")    
    processing.align_sentences(large1,large2)
    processing.fast = True
    print("\nSwitch to Fast\n")
    processing.align_sentences(large1,large2)
    #from dataBuffer import *
    #dumpStore()
