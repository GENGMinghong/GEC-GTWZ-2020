# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:29:56 2020

@author: Geng Minghong
"""
### This file is used to explain the correction created by the GEC system###

# 1. Import Packages
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer 
from nltk.corpus import wordnet
import pandas as pd

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer() 

# 2. Define Functions 
# 2.1 Get the Action: insert, remove, and replace
def get_action(s1,s2):
    m = len(s1.split())
    n = len(s2.split())
    if m>n:
        return 'remove'
    elif m<n:
        return 'insert'
    else:
        return 'replace'

# 2.2 Get the change made py GEC    
# Aim to get 3 words, the word before the error in sentence 1, the word in the error position of correct sentence and the wrong sentence   
def get_difference(s1,s2):
    temp1 = s1.split()
    temp2 = s2.split()
    for i in range(min(len(temp1),len(temp2))):
        if temp1[i] != temp2[i]:
            return temp1[i-1],temp1[i],temp2[i] # return a tuple

# 2.3 Get the category of the correction, there are 
#     This part is used to get the category of the correction
# function to convert nltk tag to wordnet tag
def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatize_sentence(sentence):
    #tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:        
            #else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)

# Get the Category of errors, there are 6 types.
def get_category(s1,s2):
    pre = get_difference(s1,s2)[0] # get the word right before the word we change
    diff = get_difference(s1,s2)[2] # get the word revised
    original = get_difference(s1,s2)[1] # get the original word before being revised
    
    diff_ratio = difflib.SequenceMatcher(None, original, diff).ratio() 
    
    #Calculate the same ratio of the original word and revised word
    p = list(set(word_tokenize(diff))-set(word_tokenize(original)))
    if p==[]:
        p = list(set(word_tokenize(original))-set(word_tokenize(diff)))    
  
    action = get_action(s1,s2)
    
    if action == 'replace':
        s = pre+' '+diff # 2 words from the revised sentence
        #tag = nltk.pos_tag(word_tokenize(s))
        tag = nltk.pos_tag(word_tokenize(lemmatize_sentence(s)))
# =============================================================================
#         the effective of pos taggin with stem is very poor, cause stem destrory the words 
#         sentence = s2
#         words = word_tokenize(sentence) 
#         list_stem = [ps.stem(word) for word in sentence.split(" ")]
#         list_stem = " ".join(list_stem)
#         nltk.pos_tag(word_tokenize(list_stem))
# =============================================================================
        if tag[0][1] in nountag and tag[1][1] in verbtag: # this method depends on the correct pos tagging, but the accuracy is not high enough.
            return 'Subject Verb Agreement'
        elif p[0] in punctuation:
                return 'Punctuation'
    else:
        if diff in article:
            return 'article'
        elif diff in preposition:
            return 'preposition'
            
        elif diff in subject_verb_agreement:
            return 'subject verb agreement'
            
        elif diff_ratio>=0.5:
            return 'Word Form'
        
# define 6 type of words
article = ['a','an','the']
preposition = ['by','to','in']
subject_verb_agreement = ['has','have','is','are','am', 'generates']
nountag = ['PRP','NN','NNS','NNP','NNPS']
verbtag = ['VBP','VBD','VBG','VBN','VBP','VBZ']
punctuation = ['.',',','!','?','..','...']


# Get The Explaination of Correction
# This function fill make use of the get_action and get_difference function.
def get_explanation(s1, s2):
    if get_category(s1,s2) == 'subject verb agreement': # now the problem is, the list of 'subject verb agreement' is only contain a certain of words. 
        print ('The form of verb', get_difference(s1,s2)[2], 'should be changaed')
    if get_category(s1,s2) == 'Punctuation':
        
    
    
#    get_explanation['Punctuation'] = 'Wrong Punctuation'

# Import Data
data = pd.read_csv('data/PowerGrammarQuestionBank.csv')
data.head()

s1 = "These devices generate huge amount of data that could be used by doctors to enhance patients' care (Burrus, 2015)."
s2 = "These devices generate, huge amount of data that could be used by doctors to enhance patients' care (Burrus, 2015)."

get_action(s1,s2)
get_difference(s1,s2)
get_category(s1,s2)
get_explanation(s1, s2)
