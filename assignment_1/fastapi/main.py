from fastapi import FastAPI, Response
from pydantic import BaseModel
import spacy
import json


app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class TextModel(BaseModel):
    text: str

@app.get("/")
def fastapi_spacy(pretty: bool = False):
    message = {"Message": "This is a pretty page built on FastAPI to access spacy NER and dependency parsing."}
    
    if pretty:
        return prettify(message)
    
    return message


@app.post("/ner")
def named_entities_recognition(text_model: TextModel, pretty: bool = False):
    doc = nlp(text_model.text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    ans = {"Entities": entities}

    if pretty:
        return prettify(ans)
    
    return ans


@app.post("/dep")
def dependency_parsing(text_model: TextModel, pretty: bool = False):
    doc = nlp(text_model.text)
    dependencies = [{"text": token.text, "dep": token.dep_, "head": token.head.text} for token in doc]

    ans = {"Dependencies": dependencies}

    if pretty:
        return prettify(ans)
    
    return ans


def prettify(result: dict):
    '''
    borrowed from given code
    '''
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type='application/json')
