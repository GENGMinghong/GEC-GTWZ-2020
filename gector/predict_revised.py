import argparse
from utils.helpers import read_lines
from gector.gec_model import GecBERTModel

def load_model():
    model = GecBERTModel(vocab_path='data/output_vocabulary',
                             model_paths=["model_path/bert_0_gector.th", "model_path/roberta_1_gector.th","model_path/xlnet_0_gector.th"],
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

def predict_for_file(input_file, output_file, batch_size=32):
    test_data = read_lines(input_file)
    predictions = []
    cnt_corrections = 0
    batch = []
    for sent in test_data:
        batch.append(sent.split())
        if len(batch) == batch_size:
            preds, cnt = model.handle_batch(batch)
            predictions.extend(preds)
            cnt_corrections += cnt
            batch = []
    if batch:
        preds, cnt = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt

    output_data = ([" ".join(x) for x in predictions])
    if output_file:
        with open(output_file, 'w') as f:
            f.write("\n".join([" ".join(x) for x in predictions]) + '\n')    
    return test_data,  output_data, cnt_corrections