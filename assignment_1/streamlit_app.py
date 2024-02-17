from collections import Counter
import streamlit as st
import pandas as pd
import altair as alt
from graphviz import Digraph
import ner_dep


example = ("Sebastian Thrun worked at Google in 2007.")

st.title("spaCy NER and Dependency")

st.sidebar.title("Setting")
view = st.sidebar.radio('select view', ['entites', 'dependencies'])
st.sidebar.info(f'Selected: {view}')

text = st.text_area('Text to process', value=example, height=100)

doc = ner_dep.SpacyDocument(text)

entities = doc.get_entities()
tokens = doc.get_tokens()
counter = Counter(tokens)
words = list(sorted(counter.most_common(30)))
dep = doc.get_dependencies()

chart = pd.DataFrame({
    'frequency': [w[1] for w in words],
    'word': [w[0] for w in words]})

bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

dep_graph = Digraph(comment='Dependency Graph')
for token in doc.get_doc():
    dep_graph.node(token.text, token.text)
    dep_graph.edge(token.head.text, token.text, label=token.dep_)

st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
            f'Total number of types: {len(counter)}', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["table", "graph"])

with tab1:
    if view == 'entites':
        st.header("entities")
        st.dataframe(entities, use_container_width=True)
    elif view == 'dependencies':
        st.dataframe(dep, use_container_width=True)

with tab2:
    if view == 'entites':
        st.header("frequency")
        st.altair_chart(bar_chart)
    elif view == 'dependencies':
        st.graphviz_chart(dep_graph)
