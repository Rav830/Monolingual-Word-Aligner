import re
from nltk.parse.dependencygraph import DependencyGraph


#this is a static data buffer, this is static because where it is being used is objects that are created and potentially destroyed

maxEntries = 0 #total to store in store
store = {}
currEntry = 0 #track of ids 

def setSize(size = 6):
    global maxEntries
    maxEntries = size

def isPresent(key):
    return key in store.keys()

#assume the data is from stanford
def bufferData(key, value):
    global store, maxEntries, currEntry
    if(key in store.keys()):
        #data already buffered
        return
    #check if we are full
    keyList = list(store.keys())
    if(len(keyList) != 0 and len(keyList) == maxEntries):
        #evict the oldest entry
        #initialize with the first entry
        minKey = keyList[0]
        minVal = store[minKey]['id']
        
        for k in store.keys():
            if(minVal > store[k]['id']):
                minVal = store[k]['id']
                minKey = k
        store.pop(minKey)
        
    #now store the data
    store[key] = {}
    #set the id
    store[key]['id'] = currEntry
    currEntry = currEntry + 1 
    
    #Extract the desired data from value
    store[key]['full'] = value
    
    #grabbing the parse
    store[key]['parse'] = value['sentences'][0]['parse']
    store[key]['parse'] = re.sub(r'\s+', ' ', store[key]['parse'])
    
    #Grabbing the pos tags, ner tags, and tokenized words
    
    store[key]['pos'] = []
    store[key]['ner'] = []
    store[key]['tokenized_words'] = []
    
    for x in value['sentences'][0]['tokens']:
        store[key]['pos'].append( (x['word'], x['pos']) )
        store[key]['ner'].append( (x['word'], x['ner']) )
        store[key]['tokenized_words'].append( x['word'] )
    
    #storing the dependency graph creation
    #reusing the code from nltk to help because it looks right
    store[key]['dependency_graph'] = generateDependencyGraph(value['sentences'][0])


#Code borrowed from nltk 3.4.5 (https://www.nltk.org/_modules/nltk/parse/corenlp.html#CoreNLPDependencyParser)
def generateDependencyGraph(data):
    return DependencyGraph(
            (
                ' '.join(n_items[1:])  # NLTK expects an iterable of strings...
                for n_items in sorted(transform(data))
            ),
            cell_separator=' ',  # To make sure that a non-breaking space is kept inside of a token.
        )
    

def transform(sentence):
    for dependency in sentence['basicDependencies']:

        dependent_index = dependency['dependent']
        token = sentence['tokens'][dependent_index - 1]

        # Return values that we don't know as '_'. Also, consider tag and ctag
        # to be equal.
        yield (
            dependent_index,
            '_',
            token['word'],
            token['lemma'],
            token['pos'],
            token['pos'],
            '_',
            str(dependency['governor']),
            dependency['dep'],
            '_',
            '_',
        )



def getData(k1, k2):
    return store[k1][k2]    

def dumpStore():
    import json
    print(json.dumps(store, indent = 2, default = lambda x: repr(x)))
    
            
    

