from fastapi import FastAPI
import spacy
from pydantic import BaseModel


app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class TextModel(BaseModel):
    text: str

@app.get("/")
def fastapi_spacy(pretty: bool = False):
    if pretty:
        return {
            "message": "This is a pretty page built on FastAPI to access spacy NER and dependency parsing."
            }
    
    return {
        "message": "This isn't a pretty page to access spaCy NER and dependency parsing"
        }

@app.post("/ner")
def named_entities_recognition(text_model: TextModel, pretty: bool = False):
    doc = nlp(text_model.text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    if pretty:
        return {"text": text_model.text,
                "entities": entities}
    
    return {"entities": entities}

@app.post("/dep")
def dependency_parsing(text_model: TextModel, pretty: bool = False):
    doc = nlp(text_model.text)
    dependencies = [{"text": token.text, "dep": token.dep_, "head": token.head.text} for token in doc]

    if pretty:
        return {"text": text_model.text,
                "dependencies": dependencies}
    
    return {"dependencies": dependencies}
