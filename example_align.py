from wordAligner import *
import sys

sentence1 = "I ate an apple. I drove a car."
sentence2 = "I ate an pear"

large1 = "I um I don't know if I would stay a fireman. Because even if society sees burning books as okay I don't know how mor-, I don't know how people morally feel about burning other people by accident? So I don't really know what I would do."
large2 = "To advance St 1's claim. Uh you have to think of it as, well I'm not saying you have to think of it as like Montag situation. But if it was as Montag, I feel like he would have more of a uh hesitant approach to it because he actually reads books and he owns books. So he would agree more with the, more with the woman than the fireman."
large3 = "Second, I think his great enjoyment of ghost stories about supernatural [xx] that he actually believes because of his strong imagination makes him utterly susceptible to Brom Bones brain which is stated in the book as that \"when he was returning one night from the neighboring village of Sing Sing, he had been overtaken by this midnight trooper; that he had offered to race with him for a bowl of punch, and should have won it too, for Daredevil beat the goblin horse all hollow, but just as they came to the church bridge, the Hessian bolted, and vanished in a flash of fire,\" which also shows that some people are able to make a really long and verbose sentence, even if the semantics seem to make no sense."
print("sentence1 = ", sentence1)
print("sentence2 = ", sentence2)



if __name__ == '__main__':

    flag = sys.argv[1]

    processing = Aligner(flag)
    
    
    #print("\nSet to Slow\n")    
    processing.align_sentences(large1,large3)
    #processing.fast = True
    #print("\nSwitch to Fast\n")
    #processing.align_sentences(large1,large3)
    #from dataBuffer import *
    #dumpStore()
