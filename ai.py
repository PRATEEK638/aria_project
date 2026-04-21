import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def extract_json(text):
    """
    Safely extract JSON from LLM output
    """
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        return None

    return text[start:end]


def get_plan(command):
    prompt = f"""
You are a strict JSON generator.

Convert the user command into JSON.

ONLY return JSON. No explanation.

Actions:
create_folder, create_file, move, delete, open, list

Understand:
- Locations: desktop, downloads, documents
- Drives: c drive, d drive, e drive
- Apps: valorant, brave, edge, spotify

Rules:
- If no location → use desktop
- Always return valid JSON
- args must always be a list

Examples:

create folder test in desktop
{{"action":"create_folder","args":["desktop/test"]}}

create file notes.txt in d drive
{{"action":"create_file","args":["d drive/notes.txt"]}}

move notes.txt to e drive
{{"action":"move","args":["desktop/notes.txt","e drive/"]}}

delete notes.txt from desktop
{{"action":"delete","args":["desktop/notes.txt"]}}

open valorant
{{"action":"open","args":["valorant"]}}

open hello.txt
{{"action":"open","args":["hello.txt"]}}

list downloads
{{"action":"list","args":["downloads"]}}

Command:
{command}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        raw_text = response.json().get("response", "").strip()

        # 🔥 Extract JSON safely
        json_text = extract_json(raw_text)

        if not json_text:
            return {"action": "unknown", "args": []}

        return json.loads(json_text)

    except json.JSONDecodeError:
        return {"action": "unknown", "args": []}

    except Exception as e:
        print(f"AI Error: {e}")
        return {"action": "unknown", "args": []}
def chat_response(command):
    prompt = f"""
You are a helpful AI assistant.

Respond normally to the user.

User: {command}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        return response.json().get("response", "I didn't understand.")

    except:
        return "AI not responding"