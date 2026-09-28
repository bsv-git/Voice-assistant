import os
from contextlib import nullcontext

MODEL_PATH = os.path.join("models", "gpt4all-model.bin")

_model = None
_model_load_error = None


def _load_model():
    global _model, _model_load_error
    if _model is not None:
        return _model
    if _model_load_error is not None:
        return None

    try:
        from gpt4all import GPT4All

        _model = GPT4All(model_name=MODEL_PATH, allow_download=False)
    except Exception as exc:
        _model_load_error = exc
        return None

    return _model


def start_realtime_session(system_prompt=None):
    model = _load_model()
    if model is None:
        return nullcontext()

    if system_prompt is None:
        return model.chat_session()

    return model.chat_session(system_prompt=system_prompt)


def generate_response(prompt):
    model = _load_model()
    if model is None:
        return "Model backend unavailable. Install gpt4all to enable speech-to-speech responses."

    response = model.generate(prompt, max_tokens=200)
    return response.strip()
