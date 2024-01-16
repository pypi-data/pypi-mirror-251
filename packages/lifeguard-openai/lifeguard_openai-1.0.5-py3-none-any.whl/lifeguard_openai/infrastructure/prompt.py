import openai

from lifeguard_openai.settings import (
    LIFEGUARD_OPENAI_TOKEN,
    LIFEGUARD_OPENAI_MODEL,
    LIFEGUARD_OPENAI_TEMPERATURE,
    LIFEGUARD_OPENAI_TOP_P,
    LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
    LIFEGUARD_OPENAI_PRESENCE_PENALTY,
    LIFEGUARD_OPENAI_MAX_TOKENS,
    LIFEGUARD_OPENAI_API_TYPE,
    LIFEGUARD_OPENAI_API_BASE,
    LIFEGUARD_OPENAI_API_VERSION,
)

openai.api_key = LIFEGUARD_OPENAI_TOKEN

if LIFEGUARD_OPENAI_API_BASE:
    openai.api_base = LIFEGUARD_OPENAI_API_BASE

if LIFEGUARD_OPENAI_API_TYPE:
    openai.api_type = LIFEGUARD_OPENAI_API_TYPE

if LIFEGUARD_OPENAI_API_VERSION:
    openai.api_version = LIFEGUARD_OPENAI_API_VERSION


def execute_prompt(prompt, options=None):
    default_options = {
        "temperature": LIFEGUARD_OPENAI_TEMPERATURE,
        "top_p": LIFEGUARD_OPENAI_TOP_P,
        "frequency_penalty": LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
        "presence_penalty": LIFEGUARD_OPENAI_PRESENCE_PENALTY,
        "max_tokens": LIFEGUARD_OPENAI_MAX_TOKENS,
    }

    if LIFEGUARD_OPENAI_API_TYPE == "azure":
        default_options["engine"] = LIFEGUARD_OPENAI_MODEL
    else:
        default_options["model"] = LIFEGUARD_OPENAI_MODEL

    if not options:
        options = {}
    options["messages"] = [
        {"role": "user", "content": prompt},
    ]
    options["stop"] = ["user:", "assistant:"]

    default_options.update(options)

    response = openai.ChatCompletion.create(**default_options)

    if response.choices:
        return response.choices[0].message.content
    return ""
