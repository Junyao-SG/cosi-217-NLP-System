"""Simple Web interface to spaCy

To see the pages point your browser at http://127.0.0.1:5000.

"""

from flask import Flask, request, render_template

import ner
import utils

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('form.html', input=open('input.txt').read())

@app.post('/')
def result():
    text = request.form['text']
    doc = ner.SpacyDocument(text)
    deps = doc.get_dependencies()
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    return render_template('result.html', markup=markup_paragraphed, dependencies=deps)


if __name__ == '__main__':

    app.run(debug=True)
