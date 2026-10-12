from contextlib import asynccontextmanager

import streamlit as st


def setup_auto_allowance():
    print("TODO Auto allowance")


@asynccontextmanager
async def lifespan(app):
    # This runs before any user connects
    setup_auto_allowance()

    yield
    # This would run after the app is shutdown


app = st.App("support/app.py", lifespan=lifespan)
