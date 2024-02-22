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
        markup_ner = doc.get_entities_with_markup()
        markup_dep = doc.get_dependencies_with_markup()

        markup_paragraphed = ''
        for line in markup_ner.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line

        return render_template('result.html',
                               markup_ner=markup_paragraphed,
                               markup_dep=markup_dep
                               )


if __name__ == '__main__':
    app.run(debug=True)
