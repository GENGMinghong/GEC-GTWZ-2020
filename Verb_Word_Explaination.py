# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:38:04 2020

@author: Geng Minghong
"""
import errant
import pandas as pd
import difflib


def get_diff(a,b):
    if len(a)>len(b): 
        res=''.join(a.split(b))             
    else: 
        res=''.join(b.split(a))             
    return res.strip()

punctuation = ['.',',','!','?','..','...','-']

def error_type(s1,s2):
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
            
def get_explanation(s1,s2):
    annotator = errant.load('en')
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    if error_type(s1,s2)=='Verb Form':
        for e in edits:
            if 'TENSE' in e.type:
                return 'Verb Tense Error'
            elif 'FORM' in e.type:
                return 'Verb Form error'
            else:
                return 'Other verb error'
    elif error_type(s1,s2)=='Word Form':
        for e in edits:
            if 'NUM' in e.type:
                return 'Noun Number error'
            elif 'ADJ' in e.type:
                return 'Adjective error'
            elif 'MORPH' in e.type:
                return 'Morphology error'
            else:
                return 'Other word form error'
            
        
data = pd.read_csv('data/PowerGrammarQuestionBank.csv')
data['give_action'] = data.apply(lambda x: get_action(x.question, x.solution),axis=1)
data['give_category'] = data.apply(lambda x: error_type(x.question, x.solution),axis=1)

s1 = 'It is forecasted that AR users will increase by another 35% over the next 5 years and millennials play a large part in that (Madigan, 2016).'
s2 = 'It is forecasted that AR users will increase by another 35% over the next 5 years and millennials will play a large part in that (Madigan, 2016).'

get_action(s1,s2)

get_explanation(s1,s2)

s3 = 'The rising incidences of stroke among young people is an issue of concern.'
s4 = 'The rising incidence of stroke among young people is an issue of concern.'

get_expla(s3,s4)
