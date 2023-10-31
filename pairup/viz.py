import inspect

import streamlit as st

from pairup.graphs import box, frames2lines, list2ll, ll2elements, plot_graph
from pairup.parsing import parse_method
from pairup.problems import TestReference, VizReference
from pairup.tasks import fetch

ss = st.session_state


def viz_main():
    # Determine which function code to use: reviewed, or initial
    use_reference = st.sidebar.checkbox("Use reference code", True)
    if use_reference:
        codestr = ss.func_bank[ss.problem]
        ss.viz_results[ss.problem] = getattr(VizReference, ss.problem, None)
        test_cases = getattr(TestReference, ss.problem, [])
    else:
        codestr = ss.review_code[ss.problem]
        test_cases = ss.test_bank[ss.problem]

    # Choose a test case to visualize
    tc_idx = st.sidebar.number_input("Test case", 0, len(test_cases) - 1)
    test_case = test_cases[tc_idx]

    def explore():
        ss.tasks.append(fetch(label="Regenerate viz", mode="viz"))

    # if not ss.viz_content[ss.problem]:
    #     st.header("Explore Code", divider="blue")
    #     st.caption("Ask the LLM to visualize your function.")
    #     st.button("Request viz", on_click=explore)
    #     st.code(inspect.getsource(func), line_numbers=True)
    #     return

    if not ss.viz_results[ss.problem]:
        try:
            viz = parse_method(ss.viz_content[ss.problem])
            st.code(viz)
        except:
            st.write("Unable to parse modified function")
            st.code(ss.viz_content[ss.problem])
            return

    st.header("Visualize Code", divider="blue")
    st.caption("View the internal state of a function.")
    left, right = st.columns([1, 1])

    # Pick a test case
    # ll = list2ll([1, 2, 3, 3, 5])

    viz_func = ss.viz_results[ss.problem]
    # Execute
    es = {"frames": [], **globals()}
    exec(viz_func, es)
    result = es[ss.problem](**test_case["inputs"])
    # result = es["reverse_linked_list"](ll)
    if "s" in test_case["inputs"]:
        plot_func = frames2lines
    else:
        plot_func = box

    with left:
        st.code(ss.viz_results[ss.problem])
        st.code(inspect.getsource(plot_func))

    with right:
        st.caption(
            "A useful visual is displayed below based on generated visualization code."
        )
        st.write(f"Test Case {test_case}")
        plot_func(es["frames"], **test_case["inputs"])

    # for idx in range(len(es["frames"])):
    #     pair = list(es["frames"][idx].values())
    #     n1, e1 = ll2elements(pair[0])
    #     n2, e2 = ll2elements(pair[1], level=1)
    #     es["frames"][idx] = (n1 + n2, e1 + e2)
    # frames = es["frames"]
    # slider = st.sidebar.slider("Frame", 0, len(frames) - 1)
    # st.write(frames[slider])
    # plot_graph(*frames[slider])
