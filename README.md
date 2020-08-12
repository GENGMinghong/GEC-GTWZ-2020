# GEC-GTWZ-2020
This is a project of Grammatical Error Correction system.<br>
Author: Geng Minghong, Tao Xinru, Wei Yuqi, Zhou Yijun. <br>
Last edit: 2020-08-12

Folder Structure:<br>

+-- gector<br>
|   +-- grammar_check.ipynb <br>
+-- post-processing<br>
|   +-- function.py<br>
+-- templates<br>
|   +-- home.html<br>
|   +-- result.html<br>
+-- notebooks<br>
|   +-- get_started_with_the_functions<br>
+-- app.py<br>
+-- .gitignore<br>

### Background
- The Use of English Quiz (UOEQ) is a test based on authentic & common errors committed by Singaporean students in their writing. However, manually generating UOEQ MCQ is very laborious. Building a system that automatically detect grammar errors for students becomes increasingly necessary.
- Many grammatical checkers on the market are charged, and the free version of grammar checkers have many errors that cannot be found.

### Motivation
SMU is looking for a tool which can:
- Identify 6 categories of student errors in the essays (articles, subject-verb agreement, prepositions, word forms, verb forms, punctuation)
- Highlight & explain these errors.

### GEC Model
We adopt the ensembled model which combines: BERT, RoBERTa and XLNet. 

Pre-trained Models and their performance
| Pretrained encoder | Confidence bias | Min error prob | CoNNL-2014 (test) | BEA-2019 (test) |
| --- | --- | --- | --- | --- | 
| BERT | 0.10 | 0.41 | 63.0 | 67.6 | 
| RoBERTa | 0.20 | 0.50 | 64.0 | 71.5 | 
| XLNet | 0.35 | 0.66 | 65.3 | 72.4 | 
| RoBERTa+XLNet | 0.24 | 0.45 | 66.0| 73.7 | 
| BERT+RoBERTa+XLNet | 0.16 | 0.40 | 66.5 | 73.6 | 

*More details can be found at https://github.com/grammarly/gector*

### Action, Error type and Explanation
Errant: Automatically annotate parallel English sentences with error type information. Specifically, given an original and corrected sentence pair, ERRANT will extract the edits that transform the former to the latter and classify them according to a rule-based error type framework.
Link: https://pypi.org/project/errant/

Original Sentence: These devices generate huge amount of data that could be used by doctors to enhance patients'
care (Burrus, 2015).

Corrected Sentence: These devices generate a huge amount of data that could be used by doctors to enhance patients'
care (Burrus, 2015).

### To Run the Codes
- Download the codes.
- Create Virtual Environment. (You may need this reference: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)
- install required packages: ```pip install -r requirements.txt``` 
- Download 3 trained model weights from https://drive.google.com/drive/folders/1Ml5d14hFYbF8nOki9zoE-1gYSC-fzD8p?usp=sharing
- Place the downloaded model weights in the folder gector/model_path. (You may need to create this folder manually)
- Run one of the notebooks. <br>
- To test the GEC model: run ```grammar_check.ipynb```
- To test the post processing functions: run ```Get_Started_with_the_functions.ipynb```
- To try the Web UI: run ```python app.py```

### To do
-	More grammatical error categories, such as adjective related errors, as well as a more detailed explanation for each kind of error type need to be involved, enhancing the interactivity of the system.
-	Data that are closer to our business application scenarios should be involved, in order to fine-tune the current pre-trained model.
-	Rule-based or other kinds of methods need to be involved to detect punctuation errors and the word form errors more accurately.
-	In terms of accepted file type, more input formats including txt or word files need be allowed, increasing the practicality of the system.
