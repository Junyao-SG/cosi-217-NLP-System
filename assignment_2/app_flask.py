from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import ner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ner_dep.db'
db = SQLAlchemy(app)


# data models
class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=0, nullable=False)
    token = db.relationship('Token', backref='author', lazy=True)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String, nullable=False)
    dependency = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=0, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)


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
  
    # flush processed entities and dependencies to database
    update_database(doc=doc)

    return render_template('result.html', markup=markup_paragraphed, dependencies=deps)


@app.get('/data')
def database():
    entities = Entity.query.all()
    return render_template('data.html', entities=entities)


def update_database(doc):
    """ helper function for updating database 
    """
    for entity, dependency in doc.get_entities_dependencies().items():

        # try to get identical entity 
        ent = Entity.query.filter_by(text=entity).first()

        # create one for non exist enity
        if not ent:
            ent = Entity(text=entity,
                         count=1
                         )
            db.session.add(ent)

        for d in dependency:
            # try to get token
            tok = Token.query.filter_by(text=d[2],
                                        dependency=d[1],
                                        head=d[0],
                                        entity_id=ent.id
                                        ).first()

            # create one token if it not exists
            if not tok:
                tok = Token(head=d[0],
                            dependency=d[1],
                            text=d[2],
                            count=1,
                            entity_id=ent.id
                            )
                db.session.add(tok)
            else:
                tok.count += 1
        
        # flush all tokens into database at first
        db.session.flush()

        # calculate frequency for the current entity
        ent.count = sum(token.count for token in ent.token) / len(entity.split(" "))

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)
