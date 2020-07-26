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
import errant

#lemmatizer = WordNetLemmatizer()
#ps = PorterStemmer() 

# 2. Define Functions 
# 2.1 Get the Action: insert, remove, and replace

# =============================================================================
# This part was weitten by Yijun. Now it is deprecated.
# def get_action(s1,s2):
#     m = len(s1.split())
#     n = len(s2.split())
#     if m>n:
#         return 'remove'
#     elif m<n:
#         return 'insert'
#     else:
#         return 'replace'
# =============================================================================

def get_action(s1,s2):
    annotator = errant.load('en')
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    for e in edits:
        if 'R:' in e.type:
            return 'replace'
        elif 'M:' in e.type:
            return 'insert'
        elif 'U:' in e.type:
            return 'remove'
        
# 2.2 Get the change made py GEC    
            
# =============================================================================
# # This part was weitten by Yijun. Now it is deprecated.
# # Aim to get 3 words, the word before the error in sentence 1, the word in the error position of correct sentence and the wrong sentence   
# def get_difference(s1,s2):
#     temp1 = s1.split()
#     temp2 = s2.split()
#     for i in range(min(len(temp1),len(temp2))):
#         if temp1[i] != temp2[i]:
#             return temp1[i-1],temp1[i],temp2[i] # return a tuple
# =============================================================================
            
def get_diff(a,b):
    if len(a)>len(b): 
        res=''.join(a.split(b))             
    else: 
        res=''.join(b.split(a))             
    return res.strip()

# 2.3 Get the category of the correction, there are 
# This part is used to get the category of the correction
# function to convert nltk tag to wordnet tag

# =============================================================================
# def nltk_tag_to_wordnet_tag(nltk_tag):
#     if nltk_tag.startswith('J'):
#         return wordnet.ADJ
#     elif nltk_tag.startswith('V'):
#         return wordnet.VERB
#     elif nltk_tag.startswith('N'):
#         return wordnet.NOUN
#     elif nltk_tag.startswith('R'):
#         return wordnet.ADV
#     else:          
#         return None
# 
# def lemmatize_sentence(sentence):
#     #tokenize the sentence and find the POS tag for each token
#     nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
#     #tuple of (token, wordnet_tag)
#     wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
#     lemmatized_sentence = []
#     for word, tag in wordnet_tagged:
#         if tag is None:
#             #if there is no available tag, append the token as is
#             lemmatized_sentence.append(word)
#         else:        
#             #else use the tag to lemmatize the token
#             lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
#     return " ".join(lemmatized_sentence)
# =============================================================================

punctuation = ['.',',','!','?','..','...','-']
def get_category(s1,s2):
    annotator = errant.load('en')
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    for e in edits:
        if 'DET' in e.type:
            return 'Articles'
        elif 'PREP' in e.type or 'PART' in e.type:
            return 'Preposition'
        elif 'PUNCT' in e.type or (e.o_str!='' and e.c_str!='' and get_diff(e.o_str,e.c_str) in punctuation) or ('-' in e.o_str or '-' in e.c_str):
            return 'Punctuation'
        elif 'VERB' in e.type:
            if 'SVA' in e.type:
                return 'Subject Verb Agreement'
            else:
                return 'Verb Form'
        elif 'NOUN' in e.type or 'ADJ' in e.type or 'MORPH' in e.type:
            return 'Word Form'
        else:
            return 'Other'

# Get the Category of errors, there are 6 types.
# =============================================================================
# def get_category(s1,s2):
#     pre = get_difference(s1,s2)[0] # get the word right before the word we change
#     diff = get_difference(s1,s2)[2] # get the word revised
#     original = get_difference(s1,s2)[1] # get the original word before being revised
#     
#     diff_ratio = difflib.SequenceMatcher(None, original, diff).ratio() 
#     
#     #Calculate the same ratio of the original word and revised word
#     p = list(set(word_tokenize(diff))-set(word_tokenize(original)))
#     if p==[]:
#         p = list(set(word_tokenize(original))-set(word_tokenize(diff)))    
#   
#     action = get_action(s1,s2)
#     
#     if action == 'replace':
#         s = pre+' '+diff # 2 words from the revised sentence
#         #tag = nltk.pos_tag(word_tokenize(s))
#         tag = nltk.pos_tag(word_tokenize(lemmatize_sentence(s)))
#         if tag[0][1] in nountag and tag[1][1] in verbtag: # this method depends on the correct pos tagging, but the accuracy is not high enough.
#                return 'Subject Verb Agreement'
#         elif p[0] in punctuation:
#                return 'Punctuation'
#     else:
#         if diff in article:
#             return 'article'
#         elif diff in preposition:
#             return 'preposition'
#         elif diff in subject_verb_agreement:
#             return 'subject verb agreement'
#         elif diff_ratio>=0.5:
#             return 'Word Form'
# =============================================================================
        
# define 6 type of words
# =============================================================================
# article = ['a','an','the']
# preposition = ['by','to','in']
# subject_verb_agreement = ['has','have','is','are','am', 'generates']
# nountag = ['PRP','NN','NNS','NNP','NNPS']
# verbtag = ['VBP','VBD','VBG','VBN','VBP','VBZ']
# punctuation = ['.',',','!','?','..','...']
# =============================================================================


# Get The Explaination of Correction
# This function fill make use of the get_action and get_difference function.
def get_explanation(s1,s2):
    annotator = errant.load('en')
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    error = get_category(s1,s2)
    if error == 'Verb Form':
        for e in edits:
            if 'TENSE' in e.type:
                return 'Verb Tense Error.'
            elif 'FORM' in e.type:
                return 'Verb Form error.'
            else:
                return 'Other verb error.'
    elif error == 'Word Form':
        for e in edits:
            if 'NUM' in e.type:
                return 'Noun Number error.'
            elif 'ADJ' in e.type:
                return 'Adjective error.'
            elif 'MORPH' in e.type:
                return 'Morphology error.'
            else:
                return 'Other word form error.'
    elif error == 'Punctuation':
        for e in edits:
            if 'M:' in e.type:
                expla = f"Consider add punctuation '{e.c_str}' in your sentence."
                return expla
            if 'R:' in e.type:
                expla = f"Consider change the punctuation into '{e.c_str}'."
                return expla
            if 'U:' in e.type:
                expla = f"Please remove the unnecessary punctuation '{e.c_str}'."
                return expla           
    elif error == 'Subject Verb Agreement':
        for e in edits:
            if True:
                expla = f"Please check the subject-verb agreement, choose the approate format for verb '{e.c_str}'."
                return expla
    elif error == 'Articles':
        for e in edits:
            if 'R:' in e.type:
                expla = f"Consider article '{e.c_str}' in front of countable or singular nouns referring to people or things what have not already been mentioned."
                return expla
            elif 'M:' in e.type:
                expla = f"Article '{e.c_str}' is required because of the countable or singular nouns referring to people or things what have not already been mentioned."
                return expla
            elif 'U:' in e.type:
                return 'No article required'
    elif error =='Preposition':
        for e in edits:
            if 'R:' in e.type:
                expla = f"Consider '{e.c_str}' to be the proper preposition."
                return expla
            elif 'M:' in e.type:
                expla = f"You need a preposition '{e.c_str}'before a noun or pronoun to show place, position, time or method."
                return expla
            elif 'U:' in e.type:
                expla = f"You don't need preposition '{e.o_str}' here, consider to remove it."
                return expla
            else:
                return 'Others'

# 3. Import Data
# The Data Imported here is the 
data = pd.read_csv('data/PowerGrammarQuestionBank_correction.csv')

data['give_action'] = data.apply(lambda x: get_action(x.question, x.correction_by_GEC),axis=1)
data['give_category'] = data.apply(lambda x: get_category(x.question, x.correction_by_GEC),axis=1)
data['give_explanation'] = data.apply(lambda x: get_explanation(x.question, x.correction_by_GEC),axis=1)

# 4. Test
# to test the explanation of verb form
s1 = 'It is forecasted that AR users will increase by another 35% over the next 5 years and millennials play a large part in that (Madigan, 2016).'
s2 = 'It is forecasted that AR users will increase by another 35% over the next 5 years and millennials will play a large part in that (Madigan, 2016).'
get_explanation(s1,s2)

# to test the explanation of noun form
s3 = 'The rising incidences of stroke among young people is an issue of concern.'
s4 = 'The rising incidence of stroke among young people is an issue of concern.'
get_explanation(s3,s4)

# to test the explanation of punction 
s5 = 'In comparison the Esplanade spends four times more on arts programmes and activities (Esplanade, 2017).'
s6 = 'In comparison , the Esplanade spends four times more on arts programmes and activities (Esplanade, 2017).'
get_explanation(s5,s6)

# to test the explanation of subject-verb agreement
s7 = 'An explanation of the statistics are required to make the data easy to understand.'
s8 = 'An explanation of the statistics is required to make the data easy to understand.'
get_explanation(s7,s8)

# to test the explanation of preposition
s9 = data['question'].iloc[8]
s10 = data['solution'].iloc[8]
get_explanation(s9,s10)

