import pandas as pd
import streamlit as st
from func_timeout import FunctionTimedOut, func_set_timeout
from pyarrow import ArrowInvalid

from pairup.configuration import Configuration as cfg
from pairup.parsing import parse_data
from pairup.tasks import fetch, fix

ss = st.session_state


def save(new_data):
    """Store the reviewed code into the bank"""

    def saver():
        ss.test_bank[ss.problem] = new_data

    return saver


def open_edit():
    """Re-enter edit mode."""
    ss.test_bank[ss.problem] = []


@func_set_timeout(cfg.TEST_CASE_TIMEOUT)
def run_func(func, input):
    try:
        result = func(input)
    except Exception as exc:
        result = str(exc)
    return result


def display_test_cases():
    results = []
    codestr = ss.code_bank[ss.problem]
    es = {**globals()}
    exec(codestr, es)
    func = es[ss.problem]
    for case in ss.test_cases:
        try:
            result = run_func(func, case.get("input", case.get("inputs")))
        except FunctionTimedOut as exc:
            result = f"Timeout({cfg.TEST_CASE_TIMEOUT}s)"
        results.append(result)
    df = pd.DataFrame(ss.test_cases)
    df["result"] = results
    st.dataframe(df, use_container_width=True)


def test_main():
    ss.test_cases = ss.test_bank[ss.problem]

    def remove_content():
        ss.test_content[ss.problem] = None

    if not ss.test_cases and not ss.test_content.get(ss.problem):
        st.header("Generate Test Cases", divider="blue")
        st.caption("Ask the LLM to create a set of test cases for your function.")
        st.button("Generate Test Cases", on_click=remove_content)
        st.code(ss.current_code)
    elif not ss.test_cases and ss.test_content.get(ss.problem):
        st.header("Review Test Cases", divider="blue")
        st.caption(
            "Edit these as necessary--generated test cases shouldn't be implicitly trusted."
        )
        left, right = st.columns([1, 1])
        test_cases, exc = parse_data(ss.test_content[ss.problem])
        # if exc is not None and not ss.test_fix[ss.problem]:
        #     ss.exceptions["test"] = str(exc)
        #     ss.tasks.append(fix(label="fix", mode="test"))
        #     ss.exceptions["test"] = None
        with left:
            df = pd.DataFrame(test_cases)
            try:
                edited_cases = st.data_editor(df, num_rows="dynamic")
            except ArrowInvalid:
                if "inputs" in df:
                    df["inputs"] = df["inputs"].astype("str")
                if "input" in df:
                    df["input"] = df["inputs"].astype("str")
                edited_cases = st.data_editor(df, num_rows="dynamic")

            new_data = edited_cases.to_dict("records")
            st.button("Regenerate Test Cases", on_click=remove_content)
            st.button("Save test cases", on_click=save(new_data))
        if ss.test_fix[ss.problem]:
            with right:
                st.text(ss.test_content[ss.problem])
                st.text(ss.test_fix[ss.problem])
    else:
        st.header("Test Cases", divider="blue")
        st.caption("These are run against live code to give responsive results.")
        left, right = st.columns([1, 1])
        with left:
            display_test_cases()
            st.button("Edit", on_click=open_edit)
