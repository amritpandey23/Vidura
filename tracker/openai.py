from openai import OpenAI

from tracker.utils2 import get_or_initialize_config


def get_completion(
    app, prompt, model="gpt-3.5-turbo", system_prompt="You are a helpful assistant"
):
    config = get_or_initialize_config(app)

    api_key = config.get("openai_configurations", {}).get("api_key")
    temperature = config.get("openai_configurations", {}).get("temperature", 0.5)
    max_tokens = config.get("openai_configurations", {}).get("max_tokens", 500)

    if not api_key:
        return ""

    client = OpenAI(api_key=api_key)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return ""
