import asyncio
import sqlite3
from datetime import date, datetime, timedelta
from typing import Callable
from zoneinfo import ZoneInfo

import support.persist as db
from support import util
from support.queries import query_strings as queries

timezone_info = ZoneInfo(util.TIMEZONE)


class WeeklyAllowanceScheduler:

    def __init__(
        self,
        connection_factory: Callable[[], sqlite3.Connection],
        deposit_allowance: Callable[[sqlite3.Connection, date], None],
    ):
        self.connection_factory = connection_factory
        self.deposit_allowance = deposit_allowance
        db.init()

    @staticmethod
    def _get_most_recent_sunday(today=None):
        if today is None:
            today = datetime.now(timezone_info).date()

        return today - timedelta(days=(today.weekday() + 1) % 7)

    def check_and_run(self, today=None):
        latest_sunday = self._get_most_recent_sunday(today)
        completed = 0

        while True:
            with self.connection_factory() as conn:
                try:
                    # Lock the database for writing before checking the log
                    conn.execute("BEGIN IMMEDIATE")

                    row = conn.execute(queries["select_latest_sunday"]).fetchone()

                    last_sunday = row[0]

                    if last_sunday is None:
                        # On the initial run start with the most recent Sunday
                        due_sunday = latest_sunday
                    else:
                        # Process every subsequent Sunday in order
                        due_sunday = date.fromisoformat(last_sunday) + timedelta(days=7)

                    if due_sunday > latest_sunday:
                        conn.rollback()
                        return completed

                    # Intentionally use the same connection for EACH allowance
                    # This ensures if anything errors we don't end up with half a process
                    self.deposit_allowance(conn, due_sunday)

                    # Finally mark that we finished this week of allowances
                    conn.execute(
                        queries["insert_new_allowance"],
                        (
                            due_sunday.isoformat(),
                            datetime.now(timezone_info).isoformat(),
                        ),
                    )

                    conn.commit()
                    completed += 1

                    print(f"Processed weekly allowance for {due_sunday.isoformat()}")

                except Exception:
                    conn.rollback()
                    raise

    async def run_loop(self, stop_event, check_interval_seconds=3600):
        # Check immediately at startup, then repeat periodically
        while not stop_event.is_set():
            try:
                completed = await asyncio.to_thread(self.check_and_run)

                if completed:
                    print(f"Processed {completed} weekly allowance period(s)")

            except Exception:
                print("Weekly allowance check failed")

            # Can wake immediately on shutdown rather than waiting an hour
            try:
                await asyncio.wait_for(
                    stop_event.wait(),
                    timeout=check_interval_seconds,
                )
            except asyncio.TimeoutError:
                pass
