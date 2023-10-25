import streamlit as st

from pairup.configuration import Configuration as cfg
from pairup.configuration import set_progress
from pairup.llm_api import stream_openai

ss = st.session_state


def overview_main():
    code = ss.current_code
    st.header("Overview", divider="blue")
    st.caption("The LLM will attempt to describe what the code is doing.")

    left, right = st.columns([1, 1])
    with left:
        st.code(ss.current_code)

    with right:
        # Display assistant response in chat message container with avatar (e.g. 🤖)
        with st.chat_message("assistant", avatar=cfg.ASST_AVATAR):
            placeholder = st.empty()
            placeholder.markdown(ss.overview_content[ss.problem])

    def stream_callback(content):
        placeholder.markdown(content + "▌")
        ss.usage += 1
        ss.overview_content[ss.problem] = content
        set_progress()

    if not ss.overview_content[ss.problem] and not cfg.DEV_TEST:
        ss.tasks.append(
            stream_openai(
                stream_callback, "", f"Explain the following Python code:\n\n{code}"
            )
        )
