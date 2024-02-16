from flask import Flask, request, render_template
import ner_dep


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html', input=open('input.txt').read())
    else:
        text = request.form['text']
        doc = ner_dep.SpacyDocument(text)
        markup = doc.get_entities_with_markup()
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        return render_template('result.html', markup=markup_paragraphed)

@app.get('/get')
def index_get():
    return render_template('form2.html', input=open('input.txt').read())

@app.post('/post')
def index_post():
    text = request.form['text']
    doc = ner_dep.SpacyDocument(text)
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    return render_template('result2.html', markup=markup_paragraphed)


if __name__ == '__main__':
    app.run(debug=True)
