"""A prototype of a programming assistant that can provide live views of data."""
import asyncio

import streamlit as st

from pairup import introduction_main, overview_main, review_main, test_main, viz_main
from pairup.configuration import Configuration as cfg
from pairup.configuration import initialize
from pairup.tasks import run_prefetch

ss = st.session_state

# Initializes the session state, layout, logging, and some widgets
initialize()


async def main():
    # Problem and Mode selectors
    title = "Choose a Sample Problem"
    options = ["None"] + list(ss.func_bank.keys())

    def reset_mode():
        ss.mode = "overview"

    st.sidebar.selectbox(
        title,
        options,
        index=0,
        key="problem",
        format_func=lambda x: x.title().replace("_", " "),
        on_change=reset_mode,
    )

    title = "Choose a Mode"
    options = cfg.MODES
    mode = st.sidebar.selectbox(
        title, options, index=0, format_func=lambda x: x.title(), key="mode"
    )

    if ss.problem == "None":
        introduction_main()
        return

    st.sidebar.checkbox("Show Content", key="show_content")
    st.sidebar.number_input("Temperature", 0.2, 1.0, step=0.1, key="temperature")
    st.sidebar.number_input(
        "API Timeout (s)", *cfg.API_TIMEOUT, step=5, key="api_timeout"
    )
    st.sidebar.number_input(
        "Test Case Timeout (ms)", *cfg.TEST_CASE_TIMEOUT, step=5, key="tc_timeout"
    )

    if mode == "overview":
        overview_main()
    elif mode == "test":
        test_main()
    elif mode == "review":
        review_main()
    elif mode == "viz":
        viz_main()

    # Show all of the active API requests
    st.sidebar.header("Tasks")

    rerun_after_tasks = False
    # Prefetch all but Overview mode (index 0) which instead will stream.
    batch = run_prefetch(cfg.MODES[1:], ss.overview_content[ss.problem])
    # Bundle any other added tasks from user-generated reruns.
    for _ in range(len(ss.tasks)):
        batch.append(ss.tasks.pop(0))
    if len(batch) > 1:
        rerun_after_tasks = True
    await asyncio.gather(*batch)
    if rerun_after_tasks:
        st.rerun()


if __name__ == "__main__":
    asyncio.run(main())
