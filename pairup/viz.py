import inspect

import streamlit as st

from pairup.graphs import list2ll, ll2elements, plot_graph
from pairup.parsing import parse_method
from pairup.tasks import fetch

ss = st.session_state


def viz_main():
    func = ss.func_bank[ss.problem]
    code = inspect.getsource(func)
    name = func.__name__

    def explore():
        ss.tasks.append(fetch(label="manual viz", mode="viz"))

    if not ss.viz_content:
        st.header("Explore Code", divider="blue")
        st.caption("Ask the LLM to visualize your function.")
        st.button("Request viz", on_click=explore)
        st.code(code, line_numbers=True)
        return

    try:
        viz = parse_method(ss.viz_content[ss.problem])
        st.code(viz)
    except:
        st.write("Unable to parse modified function")
        st.code(ss.viz_content[ss.problem])
        return

    # Pick a test case
    ll = list2ll([1, 2, 3, 3, 5])

    # Execute
    es = {"frames": [], **globals()}
    exec(viz, es)
    result = es["reverse_linked_list"](ll)

    # Process frames
    for idx in range(len(es["frames"])):
        pair = list(es["frames"][idx].values())
        n1, e1 = ll2elements(pair[0])
        n2, e2 = ll2elements(pair[1], level=1)
        es["frames"][idx] = (n1 + n2, e1 + e2)
    frames = es["frames"]
    slider = st.sidebar.slider("Frame", 0, len(frames) - 1)
    st.write(frames[slider])
    plot_graph(*frames[slider])
