"""
Lifeguard OpenAI
"""
from lifeguard.settings import SettingsManager

SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_OPENAI_API_TYPE": {
            "default": "openai",
            "description": "OpenAI API type (azure or openai)",
        },
        "LIFEGUARD_OPENAI_API_BASE": {
            "default": "",
            "description": "OpenAI API base",
        },
        "LIFEGUARD_OPENAI_API_VERSION": {
            "default": "",
            "description": "OpenAI API Version",
        },
        "LIFEGUARD_OPENAI_TOKEN": {
            "default": "",
            "description": "OpenAI token",
        },
        "LIFEGUARD_OPENAI_TEMPERATURE": {
            "default": "0",
            "type": "float",
            "description": "OpenAI temperature parameter",
        },
        "LIFEGUARD_OPENAI_MODEL": {
            "default": "gpt-35-turbo",
            "description": "OpenAI model parameter",
        },
        "LIFEGUARD_OPENAI_TOP_P": {
            "default": "0.8",
            "type": "float",
            "description": "OpenAI nucleus sampling parameter",
        },
        "LIFEGUARD_OPENAI_FREQUENCY_PENALTY": {
            "default": "0.0",
            "type": "float",
            "description": "OpenAI frequency penalty parameter",
        },
        "LIFEGUARD_OPENAI_PRESENCE_PENALTY": {
            "default": "0.0",
            "type": "float",
            "description": "OpenAI presence penalty parameter",
        },
        "LIFEGUARD_OPENAI_MAX_TOKENS": {
            "default": "200",
            "type": "int",
            "description": "OpenAI max response tokens parameter",
        },
        "LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT": {
            "default": "Can you explain the root cause for the following error?",
            "description": "OpenAI explain error prompt",
        },
    }
)

LIFEGUARD_OPENAI_API_TYPE = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_API_TYPE")
LIFEGUARD_OPENAI_API_BASE = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_API_BASE")
LIFEGUARD_OPENAI_API_VERSION = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_OPENAI_API_VERSION"
)
LIFEGUARD_OPENAI_TOKEN = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_TOKEN")
LIFEGUARD_OPENAI_TEMPERATURE = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_OPENAI_TEMPERATURE"
)
LIFEGUARD_OPENAI_MODEL = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_MODEL")
LIFEGUARD_OPENAI_TOP_P = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_TOP_P")
LIFEGUARD_OPENAI_FREQUENCY_PENALTY = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_OPENAI_FREQUENCY_PENALTY"
)
LIFEGUARD_OPENAI_PRESENCE_PENALTY = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_OPENAI_PRESENCE_PENALTY"
)
LIFEGUARD_OPENAI_MAX_TOKENS = SETTINGS_MANAGER.read_value("LIFEGUARD_OPENAI_MAX_TOKENS")
LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT"
)
