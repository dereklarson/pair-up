import inspect
import logging

import streamlit as st

from pairup.problems import Problems

ss = st.session_state


class Configuration:
    # The basic operations this demo attempts, corresponding to 'pages'.
    # MODES = ["overview", "test", "review", "viz"]
    MODES = ["overview", "test", "viz"]
    # For each (problem, mode) we store relevant data:
    #   Content - the raw output from the LLM query
    #   Results - parsed / evaluated content; mutable
    #   Bank    - results that a user explicitly saves
    #   Code    - Any changes to code state
    STORES = ["content", "results", "bank", "code", "fix"]

    DEV_TEST = False
    # DEV_TEST = True
    LOG_LEVEL = logging.DEBUG
    USAGE_LIMIT = 10000
    ASST_AVATAR = "🦆"
    API_TIMEOUT = [1, 120, 60]  # Min, Max, Default in seconds
    TEST_CASE_TIMEOUT = [10, 1000, 10]  # Min, Max, Default in milliseconds
    TEMPERATURE = [0.2, 2.0, 1.0]


def set_progress():
    usage_pct = 100 * ss.usage // Configuration.USAGE_LIMIT
    ss.progress_bar.progress(
        usage_pct, text=f"Usage: {ss.usage} / {Configuration.USAGE_LIMIT}"
    )


def initialize():
    # Wide page layout is preferable for visualization
    st.set_page_config(layout="wide")

    logging.basicConfig(
        filename="pairup.log",
        format="%(asctime)s.%(msecs)d|%(levelname)s| %(message)s",
        datefmt="%H:%M:%S",
        level=Configuration.LOG_LEVEL,
    )
    logging.info("Initialize Streamlit")

    # Load test problem code
    problems = Problems.list_all()

    # Initialize the session state
    ss.dev_test = Configuration.DEV_TEST
    ss.tasks = getattr(ss, "tasks", [])
    ss.usage = getattr(ss, "usage", 0)
    ss.message = getattr(ss, "message", "Blank")
    ss.exceptions = {mode: None for mode in Configuration.MODES}
    ss.func_bank = {name: func for name, func in problems.items()}
    # Ensure definitions for all of the session state variables
    for mode in Configuration.MODES:
        for store in Configuration.STORES:
            store_val = getattr(
                ss, f"{mode}_{store}", {name: None for name in problems.keys()}
            )
            setattr(ss, f"{mode}_{store}", store_val)

    # Have overview_code reflect the state of the codebase itself
    ss.overview_code = {
        name: inspect.getsource(func) for name, func in problems.items()
    }

    ss.progress_bar = st.sidebar.progress(0)
    set_progress()
