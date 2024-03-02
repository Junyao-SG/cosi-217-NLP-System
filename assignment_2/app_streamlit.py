from collections import Counter
from operator import itemgetter

import streamlit as st
import pandas as pd
import altair as alt

import ner
import utils


def change_view():
    print(f"Now viewing {view}")


example = (
        "Sebastian Thrun started working on self-driving cars at "
        "Google in 2007.")
example = open('input.txt').read()

st.set_page_config(layout='wide')
st.markdown('# spaCy visualization')

st.sidebar.markdown('# Settings')
view = st.sidebar.radio(
    '**Select view**',
    options=['entities', 'dependencies'],
    on_change=change_view)


text = st.text_area('Text to process', value=example, height=100)

doc = ner.SpacyDocument(text)

entities = doc.get_entities()
tokens = doc.get_tokens()
dependencies = doc.get_dependencies()


if view == 'entities':

    counter = Counter(tokens)
    words = list(sorted(counter.most_common(30)))

    chart = pd.DataFrame({
        'frequency': [w[1] for w in words],
        'word': [w[0] for w in words]})
    bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

    entities_tab, tokens_tab = st.tabs(['entities', 'tokens'])
    with entities_tab:
        st.table(entities)
    with tokens_tab:
        st.markdown(
            f'Total number of tokens: {len(tokens)}<br/>'
            f'Total number of types: {len(counter)}', unsafe_allow_html=True)
        st.altair_chart(bar_chart)


if view == 'dependencies':

    for sentence, deps in dependencies:

        deps = [d[1:] for d in deps]
        graph = utils.create_graph(deps)

        st.info(sentence)
        tab1, tab2 = st.tabs(['table', 'graph'])
        with tab1:
            st.table(deps[2:])
        with tab2:
            st.graphviz_chart(graph)
