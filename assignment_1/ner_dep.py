import io
from typing import List, Dict, Any, Tuple

import spacy

nlp = spacy.load("en_core_web_sm")


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_doc(self):
        return self.doc

    def get_tokens(self) -> list:
        return [token.lemma_ for token in self.doc]

    def get_entities(self) -> list[tuple[Any, Any, Any, str]]:
        entities = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))

        return entities

    def get_entities_with_markup(self) -> str:
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: True for e in entities}
        buffer = io.StringIO()
        for p, char in enumerate(self.text):
            if p in ends:
                buffer.write('</entity>')
            if p in starts:
                buffer.write('<entity class="%s">' % starts[p])
            buffer.write(char)
        markup = buffer.getvalue()

        return '<markup>%s</markup>' % markup

    def get_dependencies(self) -> list[dict[str, str | Any]]:
        return [{"text": token.text,
                 "dep": token.dep_,
                 "head": token.head.text} for token in self.doc]

    def get_dependencies_with_markup(self) -> str:
        dep_markup = ""
        for token in self.doc:
            dep_markup += f" {token.head.text: <30}   {token.dep_ : ^15}   {token.text : >30} \n"

        return dep_markup


if __name__ == '__main__':
    pass
