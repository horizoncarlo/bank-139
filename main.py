import asyncio
from contextlib import asynccontextmanager

import streamlit as st

import support.persist as db
from support.allowance import WeeklyAllowanceScheduler


@asynccontextmanager
async def lifespan(app):
    # This runs when the app starts up, even before a user hits the app
    scheduler = WeeklyAllowanceScheduler(
        connection_factory=db.connection,
        deposit_allowance=db.deposit_weekly_allowance,
    )

    stop_event = asyncio.Event()

    task = asyncio.create_task(
        scheduler.run_loop(
            stop_event,
            check_interval_seconds=3600,
        ),
        name="weekly-allowance-scheduler",
    )

    try:
        yield

        # Anything here runs after the app is shutdown
    finally:
        stop_event.set()
        await task


app = st.App("support/app.py", lifespan=lifespan)
