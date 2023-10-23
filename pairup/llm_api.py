import logging

import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")


class MissingKey(Exception):
    pass


if not openai.api_key:
    logging.error("No API key specified")
    raise MissingKey


async def query_openai(system: str, user: str, model: str = "gpt-3.5-turbo"):
    """Wrap the ChatCompletion API for submitting a query to OpenAI."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    response, content, usage = None, "", 0
    try:
        response = await openai.ChatCompletion.acreate(model=model, messages=messages)
        content = response.choices[0].message.content
        usage = response.usage.total_tokens
        logging.info(f"Query content:\n{content}")
    except Exception as exc:  # TODO Learn what exceptions can happen here
        logging.warning(exc)
        logging.warning(response)
    return content, usage


async def stream_openai(callback, system: str, user: str, model: str = "gpt-3.5-turbo"):
    """Wrap the ChatCompletion API for submitting a query to OpenAI."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    response, content = None, ""
    try:
        subscription = await openai.ChatCompletion.acreate(
            model=model, messages=messages, stream=True
        )
        async for response in subscription:
            content += response.choices[0].delta.get("content", "")
            callback(content)
    except Exception as exc:  # TODO Learn what exceptions can happen here
        logging.warning(exc)
        logging.warning(response)


async def list_models():
    model_obj = await openai.Model.alist()
    results = []
    for model in model_obj.data:
        if "gpt-3.5" in model.id:
            results.append(model.id)
    return results


class LLM:
    async def hello():
        prompt = f"Hi! What time is it?"
        response = await query_openai(system="", user=prompt)
        return response

    async def request_function(name: str, description: str):
        # TODO Unused currently
        system = "You are a programming assistant that generates Python code."
        prompt = f"Create a Python function called {name}. {description}\n\ndef {name}("
        response = await query_openai(system, prompt)
        return response

    async def request_review(code: str, name: str = ""):
        system = "You are a programming assistant that finds bugs in Python code."
        prompt = f"Fix any bugs in the following Python code.\n\n{code}"
        return await query_openai(system, prompt)

    async def request_test(code: str, name: str = ""):
        base_prompt = """Generate test cases for the following Python code.
        Define a variable 'test_cases' as a list of dictionaries with 'inputs'
        as one field and 'expected' as another. Do not include any text.
        """

        system = "You are a programming assistant that generates Python code."
        prompt = f"{' '.join(base_prompt.split())}\n\n{code}\n"
        return await query_openai(system, prompt)

    async def fix_test(code: str, exc: str = ""):
        system = "You are a programming assistant that generates Python code."
        prompt = f"These test cases:\n\n{code}\n\nGives an error: {exc}. Fix the error."
        return await query_openai(system, prompt)

    async def request_viz(code: str, name: str = ""):
        base_prompt = """Add code to the following Python function to capture the state
        during each iteration. Assume we can access a global variable called "frames" 
        that is a list of dictionaries."""

        # base_prompt = f"""I want to be able to step through the Python function below.
        # Assume we can access a global variable called "frames" that is a list of
        # dictionaries. Add code to "{name}" to capture the important state variables in
        # "frames". Add this code starting the line after the comment '# VIS'.
        # """

        system = "You are a programming assistant that generates Python code for visualization."
        prompt = f"{' '.join(base_prompt.split())}\n\n{code}"
        return await query_openai(system, prompt)
