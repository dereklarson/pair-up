import asyncio
import time

import streamlit as st

from pairup.configuration import Configuration as cfg
from pairup.parsing import parse_diff, parse_method, resolve_diff
from pairup.tasks import fetch
from pairup.test import display_test_cases

ss = st.session_state


def block_disp(block: list[str], clean: bool = True) -> str:
    if clean:
        block = [line[2:] for line in block]
    return "\n".join(block)


def patch_review(idx, char):
    """Choose between the options present in the diff"""
    _, lines = ss.review.pop(idx)
    # Select the lines to keep from the code block
    patch = [l for l in lines if l.startswith(char)]
    # If this is the first block and any lines remain, add a new neutral block.
    if idx == 0 and patch:
        ss.review.insert(0, [" ", patch])
        idx += 1
    # Otherwise we extend the prior neutral block
    else:
        ss.review[idx - 1][1].extend(patch)
    # Lastly, if we removed a change in between two neutral blocks, we should
    # now combine them.
    if idx < len(ss.review) and ss.review[idx][0] == " ":
        _, patch = ss.review.pop(idx)
        ss.review[idx - 1][1].extend(patch)


def accept(idx: int) -> callable:
    def append():
        patch_review(idx, "+")

    return append


def reject(idx: int) -> callable:
    def remove():
        patch_review(idx, "-")

    return remove


def save():
    """Store the reviewed code into the bank"""
    ss.review_bank[ss.problem] = "\n".join(ss.review[0][1])


def reset():
    """Reset the review state to before making any changes."""
    # ss.review = ss.review_results[ss.problem]
    ss.review_results[ss.problem] = []


def remove_content():
    ss.review_content[ss.problem] = None


def review_main():
    ss.review = ss.review_results[ss.problem]
    current_code = ss.overview_code[ss.problem]

    def review():
        ss.tasks.append(fetch(label="manual review", mode="review"))

    st.header("Review Code", divider="blue")
    left, right = st.columns([1, 1])

    if not ss.review:
        if not ss.review_content[ss.problem]:
            st.caption("Ask the LLM to find bugs and suggest replacements.")
            with left:
                st.code(current_code)
            with right:
                st.button("Request review", on_click=review)
            return
        parsed_review = parse_method(ss.review_content[ss.problem])
        if parsed_review is None:
            with left:
                st.code(current_code)
            with right:
                st.caption("The LLM made the following comments on the code:")
                with st.chat_message("assistant", avatar=cfg.ASST_AVATAR):
                    st.markdown(ss.review_content[ss.problem])
                st.button("Rerequest Review", on_click=remove_content)
            return
        ss.review_results[ss.problem] = parse_diff(current_code, parsed_review)
        ss.review = ss.review_results[ss.problem]

    ss.review_code[ss.problem] = resolve_diff(ss.review)
    left, right = st.columns([1, 1])
    with left:
        st.caption(
            "Respond to the suggested changes: choose whether to accept or reject each suggestion."
        )
        chg_idx = 0
        block_idx = 0
        for block in ss.review:
            if block[0] == " ":
                st.code(block_disp(block[1]))

            else:
                chg_idx += 1
                with st.expander(f"Change {chg_idx}", expanded=True):
                    st.code(block_disp(block[1], clean=False))
                    col1, col2, _ = st.columns([1, 1, 5])
                    with col1:
                        st.button(
                            "Accept", key=f"accept{chg_idx}", on_click=accept(block_idx)
                        )
                    with col2:
                        st.button(
                            "Reject", key=f"reject{chg_idx}", on_click=reject(block_idx)
                        )
            block_idx += 1

    with right:
        if ss.show_content:
            st.write(ss.review_content[ss.problem])
        else:
            st.caption("Track the changes in the test cases.")
            display_test_cases(ss.review_code[ss.problem])

    if chg_idx == 0:
        st.subheader("All changes handled")
        col1, col2, _ = st.columns([1, 1, 5])
        with col1:
            st.button("Save code", on_click=save)
        with col2:
            st.button("Reset Review Decisions", on_click=reset)
            st.button("Rerequest Review", on_click=remove_content)
