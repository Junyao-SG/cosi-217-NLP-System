from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import ner


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ner.db'
db = SQLAlchemy(app)

# Database Model
class NERResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String, nullable=False)
    entity = db.Column(db.String, nullable=False)
    entity_type = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


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
    
    for ent in doc.get_entities():
        ner_result = NERResult(sentence=text, entity=ent[-1], entity_type=ent[-2])
        db.session.add(ner_result)

    db.session.commit()

    return render_template('result.html', markup=markup_paragraphed, dependencies=deps)

@app.get('/data')
def database():
    all_data = NERResult.query.all()
    return render_template('data.html', all_data=all_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
