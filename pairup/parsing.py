import difflib as dl
import logging
import re


def dummy(content: str) -> str:
    return "\n".join([line.strip() for line in content.split("\n")])


import streamlit as st


def text_wrapped_parse(content: str) -> str:
    start_idx = content.index("test_cases = [") + 13
    end_idx = content.index("}\n]") + 3
    return content[start_idx:end_idx]


def match_list_of_dicts(content: str) -> str:
    matches = re.findall(r"\[\s*\{.*\},?\s*\]", content, re.DOTALL)
    return matches[-1].strip()


def last_code_block(content: str) -> str:
    matches = re.findall(r"```([^`]*)```", content, re.DOTALL)
    return matches[-1].strip()


def match_func_call(content: str) -> str:
    matches = re.findall(r"def \w+\(.*return \w+", content, re.DOTALL)
    return matches[-1].strip()


def parse_method(code_text: str) -> callable:
    for parse_func in [match_func_call, last_code_block]:
        try:
            return parse_func(code_text)
        except Exception as exc:
            logging.info(str(exc), f"using {parse_func.__name__}")


def parse_data(code_text: str) -> list:
    # We've requested a specific name for our return variable, so we can parse the
    # text content fairly simply and it should work most of the time.
    parsed = ""
    stripped = "\n".join([line.strip() for line in code_text.split("\n")])
    parse_func = match_list_of_dicts
    try:
        parsed = parse_func(stripped)
        parsed_content = eval(parsed)
        return parsed_content, None
    except Exception as exc:
        logging.info(exc, f"using {parse_func.__name__}")
        logging.info(f"Parsed: {parsed}")
        return None, str(exc)


def parse_diff(base_code, suggested_code):
    diff_curr = [line for line in base_code.split("\n")]
    diff_rev = [line for line in suggested_code.split("\n")]
    diffed = dl.ndiff(diff_curr, diff_rev)
    blocks = []
    curr = [" ", []]
    for idx, line in enumerate(diffed):
        # Accumulate neutral, +, and - blocks. Remove prefix for neutral code.
        if curr[0] == line[0]:
            # if line[0] == " ":
            #     line = line[2:]
            curr[1].append(line)
        # Finish off substitution blocks
        # Need to look ahead to see if there is a guide line
        elif curr[0] == "-" and line.startswith("+"):
            curr[1].append(line)
            curr[0] = ">"
            blocks.append(curr)
            curr = [" ", []]
        # Begin a new block
        elif line[0] in (" ", "-", "+"):
            if curr[1]:
                blocks.append(curr)
            if line[0] == " ":
                # curr = [" ", [line[2:]]]
                curr = [" ", [line]]
            else:
                curr = [line[0], [line]]
        # Guide lines should accumulate, and ignore the padding line
        elif line.startswith("?"):
            if curr[0] == " ":
                blocks[-1][1].append(line)
            else:
                curr[1].append(line)

    return blocks


def resolve_diff(diff):
    result = []
    for block in diff:
        if block[0] in " -":
            result.extend(block[1])
        elif block[0] == ">":
            result.append(block[1][0])
    return "\n".join([line[2:] for line in result])
