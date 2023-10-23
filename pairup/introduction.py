import streamlit as st

ss = st.session_state

overview_text = """
This demonstrates new potential workflows around algorithmic coding that leverage
AI capabilities, namely language modeling.

A few principles:
 * Ruthlessly shorten feedback loops.
 * Visuals are higher bandwidth than text.
 * LLMs can't handle depth, but can handle breadth.

I was motivated by recalling Bret Victor's [Inventing on Principle](https://www.youtube.com/watch?v=EGqwXt90ZqA).

Compare to [GitLab Duo](https://docs.gitlab.com/ee/user/ai_features.html#explain-selected-code-in-the-web-ui)
"""


def introduction_main():
    if ss.mode == "overview":
        st.header(
            "Welcome to Pair-Up, a concept AI programming assistant.", divider="blue"
        )
        st.markdown(overview_text)

    elif ss.mode == "review":
        st.header("Have an LLM help find bugs", divider="blue")
    elif ss.mode == "test":
        st.header("Generate Test Cases with help from an LLM", divider="blue")
    elif ss.mode == "explore":
        st.header("Visualize the problem with an AI boost", divider="blue")
