from lifeguard_openai.settings import (
    LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT,
)

from lifeguard_openai.infrastructure.prompt import execute_prompt


def _get_explanation(traceback):
    if traceback:
        response = execute_prompt(
            f"{LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT}\n\n{traceback}"
        )
        if response:
            return response
        else:
            return "No explanation available"
    return "No traceback available"


def explain_error(validation_response, _settings):
    traceback = validation_response.details.get("traceback", "")
    if isinstance(traceback, list):
        validation_response.details["explanation"] = [
            _get_explanation(entry) for entry in traceback
        ]
    else:
        validation_response.details["explanation"] = _get_explanation(traceback)
