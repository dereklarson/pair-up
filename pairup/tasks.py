import asyncio
import time

import streamlit as st
from async_timeout import timeout

from pairup.configuration import set_progress
from pairup.llm_api import LLM

ss = st.session_state


async def task(label, api_call, store, api_args):
    start = time.perf_counter()
    status = st.sidebar.status(label=label, state="running")
    try:
        async with timeout(ss.timeout):
            response = await api_call(*api_args)
            content, usage = response
            ss.usage += usage
            set_progress()
            store[ss.problem] = content
            elapsed = time.perf_counter() - start
            comp_label = f"{label} completed in {elapsed:.2f}s"
            status.update(label=comp_label, state="complete")
    except asyncio.TimeoutError:
        status.update(label=f"{label} timeout", state="complete")


async def fetch(label, mode):
    api_call = getattr(LLM, f"request_{mode}")
    store = getattr(ss, f"{mode}_content")
    await task(label, api_call, store, [ss.current_code])


async def fix(label, mode):
    api_call = getattr(LLM, f"fix_{mode}")
    store = getattr(ss, f"{mode}_fix")
    await task(label, api_call, store, [store[ss.problem], ss.exceptions[ss.mode]])


async def fake_fetch(seconds):
    async def fake_call():
        await asyncio.sleep(seconds)
        return "", 0

    await task(f"Fake {seconds}", fake_call, {}, [])


async def counter(seconds):
    ct = 0
    label = f"Count {ct} / {seconds}"
    status = st.sidebar.status(label=label, state="running")
    for i in range(seconds):
        ct += 1
        await asyncio.sleep(1)
        status.update(label=f"Count {ct} / {seconds}")

    status.update(label=f"Finished: {seconds}", state="complete")


def run_prefetch(modes):
    tasks = []
    for mode in modes:
        store = getattr(ss, f"{mode}_content")
        if not store[ss.problem]:
            if ss.dev_test:
                tasks.append(fake_fetch(5))
            else:
                tasks.append(fetch(mode, mode))
    return tasks
