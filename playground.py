import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Bank 139 - \"Real World Money. Virtually\"",
                   page_icon=":money_mouth_face:",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={
                       "About": "Some link"
                   })

if 'counter' not in st.session_state:
    st.session_state.counter = 0

@st.cache_data(show_spinner=False)
def progress_sample():
    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i + 1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'

@st.fragment()
def start_download():
    if st.button("Start Download"):
        progress_sample()

st.write("Test")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

if st.checkbox('Show dataframe'):
    st.write(df)

start_download()

def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page(page2, title="Second page", icon=":material/favorite:"),
    st.Page("page1.py", title="First page", icon="🔥"),
    st.Page(
        "https://docs.streamlit.io",
        title="Streamlit Docs",
        icon=":material/open_in_new:"
    ),
], position="hidden")

if st.button("Navigate"):
    st.switch_page("page1.py")

pg.run()

with st.container(border=True):
    if st.button("Counter Up"):
        st.session_state.counter += 1

st.write(f"Count is {st.session_state.counter}")
