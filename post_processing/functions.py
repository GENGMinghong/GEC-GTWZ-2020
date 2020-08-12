# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 17:29:56 2020

@author: Geng Minghong
"""
### This file is used to explain the correction created by the GEC system###

# 1. Import Packages
import difflib
import pandas as pd
import errant
annotator = errant.load('en')

#lemmatizer = WordNetLemmatizer()
#ps = PorterStemmer() 

# 2. Define Functions 
# 2.1 Get the Action: insert, remove, and replace
def get_action(s1,s2):
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
def get_diff(a,b):
    s= [li for li in difflib.ndiff(a, b) if li[0] != ' ']
    return s

# 2.3 Get the category of the correction, there are 
# This part is used to get the category of the correction
# Get the Category of errors, there are 6 types all together.
punc=['- .','+ .','- ,','+ ,',"- '","+ '", '- ;','+ ;','- -','+ -','-  ','+  ']
ing = ['+ i', '+ n', '+ g']

def get_category(s1,s2):
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    for e in edits:
        if 'DET' in e.type:
            return 'Articles'
        elif 'PREP' in e.type or 'PART' in e.type:
            return 'Preposition'
        elif 'PUNCT' in e.type or get_diff(e.o_str, e.c_str)[0] in punc:
            return 'Punctuation'
        elif 'VERB' in e.type or set(ing).issubset(set(get_diff(e.o_str, e.c_str))):
            if 'SVA' in e.type:
                return 'Subject Verb Agreement'
            else:
                return 'Verb Form'
        elif 'NOUN' in e.type or 'ADJ' in e.type or 'MORPH' in e.type or 'SPELL' in e.type or 'ORTH' in e.type:
            return 'Word Form'
        else:
            return 'Other'


# Get The Explaination of Correction made by our Grammar Correction Engine
# This function will make use of the get_action() and get_difference() function.
def get_explanation(s1,s2):
    orig = annotator.parse(s1)
    cor = annotator.parse(s2)
    edits = annotator.annotate(orig, cor)
    error = get_category(s1,s2)
    if error == 'Verb Form':
        for e in edits:
            if 'TENSE' in e.type:
                if 'R:' in e.type:
                    return f"Verb tense error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Verb tense error, should insert '{e.c_str}'."
                else:
                    return f"Verb tense error, should remove '{e.o_str}'."
            elif 'FORM' in e.type:
                if 'R:' in e.type:
                    return f"Verb form error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Verb form error, should insert '{e.c_str}'."
                else:
                    return f"Verb form error, should remove '{e.o_str}'."
            elif set(ing).issubset(set(get_diff(e.o_str, e.c_str))):
                if 'R:' in e.type:
                    return f"Present continuous tense, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Present continuous tense, should insert '{e.c_str}'."
                else:
                    return f"Present continuous tense, should remove '{e.o_str}'."
            else:
                if 'R:' in e.type:
                    return f"Other verb error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Other verb error, should insert '{e.c_str}'."
                else:
                    return f"Other verb error, should remove '{e.o_str}'."
    elif error == 'Word Form':
        for e in edits:
            if 'NUM' in e.type:
                if 'R:' in e.type:
                    return f"Noun Number error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Noun Number error, should insert '{e.c_str}'."
                else:
                    return f"Noun Number error, should remove '{e.o_str}'."
            elif 'ADJ' in e.type:
                if 'R:' in e.type:
                    return f"Adjective error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Adjective error, should insert '{e.c_str}'."
                else:
                    return f"Adjective error, should remove '{e.o_str}'."
            elif 'MORPH' in e.type:
                if 'R:' in e.type:
                    return f"Morphology error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Morphology error, should insert '{e.c_str}'."
                else:
                    return f"Morphology error, should remove '{e.o_str}'."
            elif 'ORTH' in e.type:
                if 'R:' in e.type:
                    return f"Orthography error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Orthography error, should insert '{e.c_str}'."
                else:
                    return f"Orthography error, should remove '{e.o_str}'."
            else:
                if 'R:' in e.type:
                    return f"Other word form error, should replace '{e.o_str}' with '{e.c_str}'."
                elif 'M:' in e.type:
                    return f"Other word form error, should insert '{e.c_str}'."
                else:
                    return f"Other word form error, should remove '{e.o_str}'."
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

def get_highlighted_sentence(s1,s2):
    seqm = difflib.SequenceMatcher(None,s1,s2)
    """Unify operations between two compared strings seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []
    for i,j in enumerate(seqm.get_opcodes()):
        opcode,a0,a1,b0,b1 = j
        if opcode == 'equal':
            output.append(seqm.a[a0:a1].strip())
        elif opcode == 'insert':
            insert = seqm.b[b0:b1]
            if seqm.b[b0-1] == " " or seqm.b[b0] == " ":
                output.append("<insert_word>")
            else:
                v = a0
                while seqm.a[v-1]!=" ":
                    v-=1
                if output and seqm.a[v:a0] in output[-1]:
                    output[-1] = output[-1].replace(seqm.a[v:a0],"").strip()
                output.append("<insert>" + seqm.a[v:a0] + "</insert>")
        elif opcode == 'delete':
            v = a0
            if seqm.a[v-1]!=" ":
                while seqm.a[v-1]!=" ":
                    v-=1
                if output and seqm.a[v:a0] in output[-1]:
                    output[-1] = output[-1].replace(seqm.a[v:a0],"").strip()
            output.append("<delete>" + seqm.a[v:a1] + "</delete>")
            
        elif opcode == 'replace':
            v = a0
            if seqm.a[v-1]!=" ":
                while seqm.a[v-1]!=" ":
                    v-=1
                if output and seqm.a[v:a0] in output[-1]:
                    output[-1] = output[-1].replace(seqm.a[v:a0],"").strip()
            output.append("<replace>" + seqm.a[v:a1] + "</replace>") 
    output = " ".join(output).split(" ")
    indices = [i for i, x in enumerate(output) if x == "<insert_word>"]
    if indices:
        for indice in indices:
            output[indice-1] = "".join(["####",output[indice-1]]) 
            output[indice+1] = "".join([output[indice+1],"###"])
        output = [x for x in output if x!="<insert_word>"]
    output = ' '.join(output)
    output = output.replace("<replace>","####").replace("</replace>","###")
    output = output.replace("<insert>","####").replace("</insert>","###")
    output = output.replace("<delete>","####").replace("</delete>","###")
    return output
