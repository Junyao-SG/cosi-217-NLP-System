from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import ner


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sent_ner.db'
db = SQLAlchemy(app)

# database models
class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    ner = db.relationship('NER', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"Sentence( sentence={self.sentence} timestamp={self.timestamp})"

class NER(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String, nullable=False)
    entity_type = db.Column(db.String, nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'), nullable=False)

    def __repr__(self):
        return f"NER( entities={self.entity} type={self.entity_type}')"

@app.get('/')
def index():
    with open('input.txt', 'r') as file:
        input_text = file.read()
    return render_template('form.html', input=input_text)

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
    
    for sent_ent in doc.get_entities_sentence_wise():
        sent = Sentence(sentence=sent_ent[0])
        db.session.add(sent)

        sent = Sentence.query.filter_by(sentence=sent_ent[0], ner=None).first()
        for ent in sent_ent[1]:
            ner_ = NER(entity=ent[1], entity_type=ent[0], sentence_id=sent.id)
            db.session.add(ner_)

    db.session.commit()

    return render_template('result.html', markup=markup_paragraphed, dependencies=deps)

@app.get('/data')
def database():
    sentences = Sentence.query.all()
    return render_template('data.html', sentences=sentences)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
