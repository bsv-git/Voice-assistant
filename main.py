from datetime import datetime, timezone

from history import save_interaction
from models.model import generate_response, start_realtime_session
from stt import transcribe_audio
from tts import speak

EXIT_COMMANDS = {"exit", "quit", "stop"}


def route_backend_agent(user_text):
    normalized = user_text.strip().lower()
    if "time" in normalized:
        return f"Current time: {datetime.now(timezone.utc).isoformat()}"

    if normalized.startswith("agent:echo "):
        return user_text.split(" ", 1)[1]

    return None


def run_assistant(max_turns=None):
    completed_turns = 0

    with start_realtime_session():
        while True:
            if max_turns is not None and completed_turns >= max_turns:
                break

            user_text = transcribe_audio()
            if user_text is None:
                continue

            user_text = user_text.strip()
            if not user_text:
                continue

            if user_text.lower() in EXIT_COMMANDS:
                break

            print(f"You said: {user_text}")

            response = route_backend_agent(user_text)
            if response is None:
                response = generate_response(user_text)

            speak(response)
            save_interaction(user_text, response)
            completed_turns += 1


if __name__ == "__main__":
    run_assistant()
