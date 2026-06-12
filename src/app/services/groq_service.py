import json

from groq import Groq

from src.app.core.config import get_settings
from src.app.schemas.voice import InstructionPayload

# The system prompt: this is the most important part of the whole project.
# It tells the LLM exactly how to behave and what shape to respond in.
SYSTEM_PROMPT = """You are a routing engine for a voice-controlled task list API.

You receive a plain-text transcription of something a user said out loud.
Your job is to translate it into a single API call.

You must respond with ONLY a valid JSON object — no explanation, no markdown,
no code fences, no extra text. Just the raw JSON.

The JSON must have exactly these three keys:
  "endpoint": the API path as a string
  "method":   the HTTP method as a string (GET, POST, PUT, PATCH, or DELETE)
  "params":   an object with any parameters needed (use {} if none)

Available actions:
  - List all tasks        -> {"endpoint": "/tasks", "method": "GET", "params": {}}
  - Create a task         -> {"endpoint": "/tasks", "method": "POST", "params": {"title": "<the task text>"}}
  - Replace a task        -> {"endpoint": "/tasks/<id>", "method": "PUT", "params": {"title": "<text>", "done": <true|false>}}
  - Update a task         -> {"endpoint": "/tasks/<id>", "method": "PATCH", "params": {"done": <true|false>}}
  - Delete a task         -> {"endpoint": "/tasks/<id>", "method": "DELETE", "params": {}}

When the user wants to add something, extract just the task itself as the title.
For example, "add buy groceries to my list" -> title is "Buy groceries".

Respond with only the JSON object."""


def get_instruction_from_text(transcription: str) -> InstructionPayload:
    settings = get_settings()
    client = Groq(api_key=settings.groq_api_key)

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcription},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)
    return InstructionPayload(**data)
