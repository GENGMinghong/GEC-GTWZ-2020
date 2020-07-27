from flask import Flask, request, render_template,jsonify
from post_processing.functions import *
from gector.predict_revised import prediction
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      input_text = request.form['input_text']
      output_text = prediction(input_text)
      action = get_action(input_text,output_text)
      category =  get_category(input_text,output_text)
      explaination = get_explanation(input_text,output_text)
      input_highlight = get_highlighted_sentence(input_text,output_text)

      result = [input_highlight,output_text,action,category,explaination]

      return render_template("result.html",result = result)

if __name__ == '__main__':
    app.run(debug=True)