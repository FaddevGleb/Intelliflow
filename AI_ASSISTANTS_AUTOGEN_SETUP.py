import os
config_list = [{
    "model": "openai/gpt-oss-20b:free",
    "api_type": "together",
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "base_url": "https://openrouter.ai/api/v1",
    "max_tokens": 1024,
    "temperature": 0.7
}]