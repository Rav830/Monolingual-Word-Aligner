import nltk

from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser

#from nltk.parse.stanford import StanfordParser, StanfordDependencyParser
#from nltk.tag.stanford import StanfordPOSTagger
#from nltk.tag import StanfordNERTagger

from nltk.tokenize import sent_tokenize#, word_tokenize

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from alignerConfig import *

from dataBuffer import *

import requests

class Text_processing:


    def __init__(self):
        
        # user need to download Stanford Parser, NER and POS tagger from stanford website
        #parserJar = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-parser-full-2017-06-09/stanford-parser.jar"
        #parserModel = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar"
        
        self.fullModule = CoreNLPParser(url='http://localhost:9000')
        self.customProperties = {'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse'}
        
        
        
        #self.constituent_parse_tree = CoreNLPParser(url='http://localhost:9000')

        # StanfordParser(path_to_jar=parserJar, path_to_models_jar=parserModel)
        # user need to set as environment variable
        #self.stanford_dependency =  CoreNLPDependencyParser(url='http://localhost:9000')
        #StanfordDependencyParser(path_to_jar=parserJar, path_to_models_jar=parserModel)
        # #user need to set as environment variable
        self.lemma = WordNetLemmatizer()
        
        ##self.ner = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
        #self.pos_tag = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
        
        
        #self.home = '/home/ramesh'
        #user needs to download stanford packages and change directory
        #nerModelPath = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz"
        #nerJarPath = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-ner-2017-06-09/stanford-ner.jar"
        #self.ner = StanfordNERTagger(model_filename = nerModelPath,path_to_jar=nerJarPath)
        #posModelPath = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger"
        #posJarPath = "/home/rav/Development/Semantic-Textual-Similarity/monolingualWordAligner/stanfordModels/stanford-postagger-2017-06-09/stanford-postagger-3.8.0.jar"
        #self.pos_tag = StanfordPOSTagger(model_filename = posModelPath,path_to_jar=posJarPath)
        
        
        self.CharacterOffsetEnd = 0 
        self.CharacterOffsetBegin = 0
        
        
        #this try block is just to check and make sure the server is up and running by 
        #parsing a random sentence 
        try:
            self.parser("A random sentence")
        except requests.ConnectionError as err:
            print("The server doesn't seem to be running, make sure you start it")
            raise SystemExit

    '''
    Input: sentence
    Returns: 
    '''


    def parser(self,sentence):


        self.parseResult = {'parseTree':[], 'text':[], 'dependencies':[],'words':[] }
        
        #this is Rav hijacking the process and precomputing a lot of info and the sending it to a buffer
        
        #the process does a sent_tokenize for the text and then passes each sentence into the stanford Parse
        
        sentences = sent_tokenize(sentence)
        for sent in sentences:
            if(not isPresent(sent)):
                toBuffer = self.fullModule.api_call(sent,  properties = self.customProperties)
                bufferData(sent, toBuffer)

        
        
        parseText = self.get_parseText(sentence, sentences)
        # print "sentences ", sentences
        # if source/target sent consist of 1 sentence 
        if len(sentences) == 1:
            return parseText
        
        wordOffSet = 0 # offset is number of words in first sentence 

        # if source/target sentence has more than 1 sentence

        for i in range(len(parseText['text'])):
            if i > 0:

                for j in range(len(parseText['dependencies'][i])):
                    # [root, Root-0, dead-4]
                    for k in range(1,3):
                        tokens = parseText['dependencies'][i][j][k].split('-')

                        if tokens[0] == 'Root':
                            newWordIndex = 0

                        else:
                            if not tokens[len(tokens)-1].isdigit():
                                continue 

                            newWordIndex = int(tokens[len(tokens)-1]) + wordOffSet

                        if len(tokens) == 2:

                             parseText['dependencies'][i][j][k] = tokens[0]+ '-' + str(newWordIndex)
                                                
                        else:
                            w = ''
                            for l in range(len(tokens)-1):
                                w += tokens[l]
                                if l<len(tokens)-2:
                                    w += '-'

                            parseText['dependencies'][i][j][k] = w + '-' + str(newWordIndex)

            wordOffSet += len(parseText['words'][i])

        return parseText


    '''
    Input: parserResult 
    Returns: [[charBegin,charEnd], wordIndex(starts from 1), word, word_lemma]] 
    '''


    def get_lemma(self,parserResult):


        res = []        
        wordIndex = 1
        for i in range(len(parserResult['words'])):
            
            for j in range(len(parserResult['words'][i])):
                
                tag = [ [parserResult['words'][i][j][1]['CharacterOffsetBegin'], parserResult['words'][i][j][1]['CharacterOffsetEnd']], wordIndex,parserResult['words'][i][j][0] ,parserResult['words'][i][j][1]['Lemma'] ]
                wordIndex += 1
                res.append(tag)

        return res



    '''
    Using Stanford POS Tagger
    Input: parserResult 
    Returns: [[charBegin,charEnd], wordIndex(starts from 1), word, word_POS]] 
    '''


    def combine_lemmaAndPosTags(self,parserResult):

        res = []
        
        wordIndex = 1
        for i in range(len(parserResult['words'])):
            
            for j in range(len(parserResult['words'][i])):
                
                tag = [ [parserResult['words'][i][j][1]['CharacterOffsetBegin'], parserResult['words'][i][j][1]['CharacterOffsetEnd']], wordIndex,parserResult['words'][i][j][0] ,parserResult['words'][i][j][1]['Lemma'] ,parserResult['words'][i][j][1]['PartOfSpeech'] ]
                wordIndex += 1
                res.append(tag)

        return res


    '''
    Input: parserResult
    Returns: ([charOffsetBegin,charOffsetEnd], wordindex,word, NER ])
    '''


    def nerWordAnnotator(self,parserResult):

        res = []
        
        wordIndex = 1
        for i in range(len(parserResult['words'])):
            
            for j in range(len(parserResult['words'][i])):
                
                tag = [ [parserResult['words'][i][j][1]['CharacterOffsetBegin'], parserResult['words'][i][j][1]['CharacterOffsetEnd']], wordIndex,parserResult['words'][i][j][0] ,parserResult['words'][i][j][1]['NamedEntityTag'] ]
                # print "tag ", tag
                wordIndex += 1
                # if there is valid named entity then add in list
                if tag[3] != 'O':

                    res.append(tag)

        return res


    '''
    Input : ParserResult
    Returns : list containing NamedEntites
    1. Group words in same list if they share same NE (Location), 
    2. Save other words in list that have any entity
    '''


    def get_ner(self,parserResult):


        nerWordAnnotations = self.nerWordAnnotator(parserResult) #[[ [charbegin,charEnd], wordIndex, word, NE ]]
        namedEntities = []
        currentWord = []
        currentCharacterOffSets = []
        currentWordOffSets = []

        for i in range(len(nerWordAnnotations)):

            if i == 0:

                currentWord.append(nerWordAnnotations[i][2]) # word having NE
                currentCharacterOffSets.append(nerWordAnnotations[i][0]) # [begin,end]
                currentWordOffSets.append(nerWordAnnotations[i][1]) # Word Index
                # if there is only one ner Word tag
                if (len(nerWordAnnotations) == 1):
                    namedEntities.append([ currentCharacterOffSets, currentWordOffSets, \
                        currentWord, nerWordAnnotations[i-1][3] ])
                    # print "named Entities ", namedEntities
                    break 
                continue
            # if consecutive tags have same NER Tag, save them in one list
            if nerWordAnnotations[i][3] == nerWordAnnotations[i-1][3] and \
                    nerWordAnnotations[i][1] == nerWordAnnotations[i-1][1] + 1:
                
                currentWord.append(nerWordAnnotations[i][2]) # word having NE
                currentCharacterOffSets.append(nerWordAnnotations[i][0]) # [begin,end]
                currentWordOffSets.append(nerWordAnnotations[i][1]) # Word Index

                if i == (len(nerWordAnnotations) - 1):
                    namedEntities.append([ currentCharacterOffSets, \
                        currentWordOffSets, currentWord, nerWordAnnotations[i][3] ])
            # if consecutive tags do not match
            else:

                namedEntities.append([ currentCharacterOffSets, \
                        currentWordOffSets, currentWord, nerWordAnnotations[i-1][3] ])
                currentWord = [nerWordAnnotations[i][2]]
                # remove everything from currentCharacterOffSets and currentWordOffSets
                currentCharacterOffSets = []
                currentWordOffSets = []
                # add charac offsets and currentWordOffSets of current word
                currentCharacterOffSets.append(nerWordAnnotations[i][0])
                currentWordOffSets.append(nerWordAnnotations[i][1])

                # if it is last iteration then update named Entities
                if i == len(nerWordAnnotations)-1:
                    namedEntities.append([ currentCharacterOffSets, currentWordOffSets, \
                            currentWord, nerWordAnnotations[i][3] ])
        #sort out according to len of characters in ascending order
        namedEntities = sorted(namedEntities, key=len)

        return namedEntities


    '''
    Input: Word(Word whose NE is not found), NE(word already have NE Tag) 
    Returns: Boolean; True if word is acronym
                    False if word is not acronym
    '''


    def is_Acronym(self,word,NE):


        queryWord = word.replace('.','')
        # If all words of queryWord is not capital or length of word != 
                #length of NE(word already have NE Tag) or 
           #  if word is 'a' or 'i' 
        if not queryWord.isupper() or len(queryWord) != len(NE) or queryWord.lower() in ['a', 'i']:
            return False

        acronym = True

        #we run for loop till length of query word(i.e 3)(if word is 'UAE')
        #Compare 1st letter(U) of query word with first letter of first element in named entity(U = U(united))
        # again we take second letter of canonical word (A) with second element in named entity(Arab)
        # and so on 
        for i in range(len(queryWord)):
            # print "queryword[i], NE ", queryWord, NE
            if queryWord[i] != NE[i][0]:
                acronym = False
                break

        return acronym


    '''
    Input: one or more sentences in a string
    Returns: parse(    {ParseTree, text, Dependencies, 
      'word : [] NamedEntityTag, CharacterOffsetEnd, 
              CharacterOffsetBegin, PartOfSpeech, Lemma}']}) 
              sentence and
    '''


    def get_parseText(self,sentence, tokenized_sentence):

        self.count = 0
        self.length_of_sentence = [] # stores length of each sentence
        # print "len of tokenized ",len(tokenized_sentence)
        if (len(tokenized_sentence) == 1):
            self.count += 1
            for i in tokenized_sentence:
                parse = self.get_combine_words_param(i)
        else:
            tmp = 0
            for i in tokenized_sentence:
                self.count += 1
                parse = self.get_combine_words_param(i)
                s = len(i) + tmp
                self.length_of_sentence.append(s)
                tmp = s

        return parse
        

    '''
    Input: sentence
    Return: constituency tree that represents relations between sub-phrases in sentences
    '''


    def get_constituency_Tree(self,sentence):
        '''
        sentence = sent_tokenize(sentence)
        constituency_parser = self.constituent_parse_tree.raw_parse_sents(sentence)
        #]
        
        #this seems to be converting a tree object into a string
        for parser in constituency_parser:
            for sent in parser:
                tree = str(sent)
        parse_string = ' '.join(str(tree).split()) 
        
        print(parse_string)
        '''
        parse_string = getData(sentence, "parse") 
        return parse_string


    '''
    Input: sentence
    returns: relation between words with their index
    '''    


    def get_dependencies(self,sentence):

        dependency_tree = []
        depGraph = getData(sentence, 'dependency_graph')
        token = getData(sentence, "tokenized_words")

        # Find root(head) of the sentence 
        for k in depGraph.nodes.values():
            if k["head"] == 0:
                dependency_tree.append([str(k["rel"]), "Root-" + str(k["head"]), str(k["word"]) 
                    + "-" + str(k["address"]) ])            
        # Find relation between words in sentence
        for triple in depGraph.triples():
            index_word = token.index(triple[0][0]) + 1 # because index starts from 0 
            index2_word = token.index(triple[2][0]) + 1
            dependency_tree.append([str(triple[1]),str(triple[0][0]) + "-" + str(index_word),\
                             str(triple[2][0]) + "-" + str(index2_word)])
        
        return dependency_tree


    '''
    Input: sentence, word(of which offset to determine)
    Return: [CharacterOffsetEnd,CharacterOffsetBegin] for each word
    '''


    def get_charOffset(self,sentence, word):

        # word containing '.' causes problem in counting

        CharacterOffsetBegin = sentence.find(word)
        CharacterOffsetEnd = CharacterOffsetBegin + len(word)
        
        return [CharacterOffsetEnd,CharacterOffsetBegin]


    '''
    Input: sentence
    Returns: dictionary: 
    {ParseTree, text, Dependencies, 
      #'word : [] NamedEntityTag, CharacterOffsetEnd, CharacterOffsetBegin, PartOfSpeech, Lemma}']}
    '''


    def get_combine_words_param(self,sentence):
        

        words_in_each_sentence = []
        words_list = [] 
        #tokenized_words = word_tokenize(sentence)
        tokenized_words = getData(sentence, "tokenized_words")#list(self.constituent_parse_tree.tokenize(sentence))
        posTag = getData(sentence, "pos")#self.pos_tag.tag(tokenized_words)
        ner =  getData(sentence, "ner")#self.ner.tag(tokenized_words)
        
        
        # if source sentence/target sentence has one sentence
        if (self.count == 1):
            for i in range(len(tokenized_words)):
                word_lemma = str()
                word = tokenized_words[i]
                name_entity = ner[i]
                word_posTag = posTag[i][-1]  # access tuple [(United, NNP),..]
                # print "word and pos tag ", word, word_posTag[0]    
                #wordNet lemmatizer needs pos tag with words else it considers noun
                if (word_posTag[0] == 'V'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.VERB)

                elif (word_posTag[0] == 'J'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.ADJ)

                elif (word_posTag[0:1] == 'RB'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.ADV)

                else:
                    word_lemma = self.lemma.lemmatize(tokenized_words[i])

                self.CharacterOffsetEnd, self.CharacterOffsetBegin = self.get_charOffset(sentence,tokenized_words[i])
                

                words_list.append([word, {"NamedEntityTag" : str(name_entity[1]),
                    "CharacterOffsetEnd" : str(self.CharacterOffsetEnd), "CharacterOffsetBegin" : str(self.CharacterOffsetBegin) 
                    ,"PartOfSpeech" : str(word_posTag) , "Lemma" : str(word_lemma)}])

            self.parseResult['parseTree'] = [self.get_constituency_Tree(sentence)]
            self.parseResult['text'] = [sentence]
            self.parseResult['dependencies'] = [self.get_dependencies(sentence)]
            self.parseResult['words'] = [words_list]

        else:

            for i in range(len(tokenized_words)):
                word = tokenized_words[i]
                name_entity = ner[i] 
                word_posTag = posTag[i][-1]

                if (word_posTag[0] == 'V'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.VERB)

                elif (word_posTag[0] == 'J'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.ADJ)

                elif (word_posTag[0:1] == 'RB'):
                    word_lemma = self.lemma.lemmatize(tokenized_words[i], wordnet.ADV)

                else:
                    word_lemma = self.lemma.lemmatize(tokenized_words[i])

                end, begin = self.get_charOffset(sentence,tokenized_words[i])
                end = end + self.length_of_sentence[self.count-2] + 1
                begin = begin + self.length_of_sentence[self.count-2] + 1    
                words_list.append([word, {"NamedEntityTag" : str(name_entity[1]),
                    "CharacterOffsetEnd" : str(end), "CharacterOffsetBegin" : str(begin) 
                    ,"PartOfSpeech" : str(word_posTag) , "Lemma" : str(word_lemma)}])
            self.parseResult['parseTree'].append(self.get_constituency_Tree(sentence))
            self.parseResult['text'].append(sentence)
            self.parseResult['dependencies'].append(self.get_dependencies(sentence))
            self.parseResult['words'].append(words_list)

        return self.parseResult
