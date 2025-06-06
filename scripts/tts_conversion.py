import requests
import os
from api_keys import ELEVENLABS_API_KEY, VOICE_IDS

def text_to_speech(character, text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_IDS[character]}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.85
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"TTS error: {response.status_code}, {response.text}")
