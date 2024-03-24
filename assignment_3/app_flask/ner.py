"""ner.py

Run spaCy NER over an input string and insert XML tags for each entity.

"""

import io
import spacy
from collections import defaultdict


nlp = spacy.load("en_core_web_sm")


class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self) -> list:
        return [token.lemma_ for token in self.doc]

    def get_entities(self) -> list:
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

    def get_dependencies(self) -> list:
        """Returns a list of tuples where each tuple contains the sentence and a
        list of dependencies."""
        dependencies = []
        for sentence in self.doc.sents:
            sent_deps = []
            for token in sentence:
                sent_deps.append((token.is_sent_start, 
                                  token.head.text, 
                                  token.dep_, 
                                  token.text))
            dependencies.append((str(sentence), sent_deps))
        return dependencies
    

    def get_entities_dependencies(self):
        """ return a dictionary with structure {str0: [str1, str2, str3]} """
        ent_dep = defaultdict(list)

        for entity in self.doc.ents:
            for token in entity:
                ent_dep[entity.text].append([token.head.text, 
                                             token.dep_, 
                                             token.text])
                
        return ent_dep


if __name__ == '__main__':

    example = (
        "Sebastian Thrun started working on self-driving cars at "
        "Google in 2007. Sue did not.")

    doc = SpacyDocument(example)
    print(doc.get_tokens())
    for entity in doc.get_entities():
        print(entity)
    print(doc.get_entities_with_markup())

    print(doc.get_entities_dependencies())
    print(doc.get_entities())
