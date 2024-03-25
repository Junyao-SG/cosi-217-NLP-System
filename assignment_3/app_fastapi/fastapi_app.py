from fastapi import FastAPI, Response
from pydantic import BaseModel
import ner_dep
import json


app = FastAPI()


class TextModel(BaseModel):
    text: str


@app.get('/')
def index(pretty: bool = False):
    url = "http://localhost:8050"
    answer = {
        "description": "Interface to the spaCy entity extractor",
        "get named entities": f'curl -H "Content-Type: application/json" -d@input.json {url}/ner',
        "get dependencies": f'curl -H "Content-Type: application/json" -d@input.json {url}/dep'
        }
    if pretty:
        answer = prettify(answer)
    return answer


@app.post("/ner")
def named_entities_recognition(text_model: TextModel, pretty: bool = False):
    doc = ner_dep.SpacyDocument(text_model.text)
    entities = doc.get_entities()

    ans = {"Entities": entities}
    if pretty:
        return prettify(ans)

    return ans


@app.post("/dep")
def dependency_parsing(text_model: TextModel, pretty: bool = False):
    doc = ner_dep.SpacyDocument(text_model.text)
    dependencies = doc.get_dependencies()

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
