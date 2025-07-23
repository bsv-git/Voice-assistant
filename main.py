# main.py (flow sketch)
from stt import transcribe_audio
from models.model import generate_response
from tts import speak
#from skills import route_intent
from history import save_interaction

def run_assistant():
    user_text = transcribe_audio()
    print(f"You said: {user_text}")
    response = generate_response(user_text)
    
    # skill_output = route_intent(user_text)
    # if skill_output:
    #     response = skill_output
    # else:
    #     response = generate_response(user_text)

    speak(response)
    save_interaction(user_text, response)

if __name__ == "__main__":
    run_assistant()
