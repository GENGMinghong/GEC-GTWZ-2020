import argparse
from gector.helpers import read_lines
from gector.gec_model import GecBERTModel

def load_model():
    model = GecBERTModel(vocab_path='gector/data/output_vocabulary',
                             model_paths=["gector/model_path/bert_0_gector.th", "gector/model_path/roberta_1_gector.th","gector/model_path/xlnet_0_gector.th"],
                             max_len=50, min_len=3,
                             iterations=5,
                             min_error_probability=0,
                             min_probability=0,
                             lowercase_tokens=0,
                             model_name=['bert', 'roberta', 'xlnet'],
                             special_tokens_fix=1,
                             log=False,
                             confidence=0,
                             is_ensemble=1)
    return model
                      
model = load_model()

def prediction(input_sentence):
    
    cnt_corrections = 0
    
    preds, cnt = model.handle_batch([input_sentence.split()])

    output_sentence = " ".join(preds[0])
     
    return output_sentence