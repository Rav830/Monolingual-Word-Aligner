import json
from nltk.parse import CoreNLPParser
#from nltk.parse import GenericCoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
print("this is me figuring out how to best use stanford nlp")

easySent = "This is an easy sentence."
twoSent = "I ate an apple.\nI drove a car."
hardSent = "This is a hard a hard sentence."
# Lexical Parser
#parser = CoreNLPParser(url='http://localhost:9000')
#dependency =  CoreNLPDependencyParser(url='http://localhost:9000')
#ner = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
#pos_tag = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

full = CoreNLPParser(url='http://localhost:9000')

newProp = {'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse'}
print(json.dumps(full.api_call(twoSent, properties = newProp), indent = 2))
