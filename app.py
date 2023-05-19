from flask import Flask, request, render_template
from functions import correction_automated

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def spell_check():
    result = None
    if request.method == 'POST':
        word = request.form['word']
        corrected_word = correction_automated(word)
        result = corrected_word
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
