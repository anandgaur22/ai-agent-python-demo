"""
tools.py - The agent's "hands". These are just normal Python functions.

get_weather -> Live weather from the FREE Open-Meteo API (no key needed)
calculator  -> Solves a math expression
get_time    -> Returns the current date and time
save_note   -> Writes a note to notes.txt (shows the agent can take ACTIONS)
"""
import datetime
import json
import urllib.parse
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode())


def get_weather(city: str) -> str:
    try:
        q = urllib.parse.quote(city)
        geo = _get_json(f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1")
        if not geo.get("results"):
            return f"Could not find a city named '{city}'"
        place = geo["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        data = _get_json(
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        c = data["current"]
        return (f"{place['name']}: {c['temperature_2m']}°C, "
                f"humidity {c['relative_humidity_2m']}%, wind {c['wind_speed_10m']} km/h")
    except Exception:
        # If the internet fails during a workshop, the demo should not stop
        fake = {"delhi": "34°C, sunny", "mumbai": "29°C, rainy", "bangalore": "24°C, cloudy"}
        return fake.get(city.lower(), "25°C, clear sky") + " (offline sample data)"


def calculator(expression: str) -> str:
    try:
        # For demo purposes only. Never use eval() in production code.
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


def get_time() -> str:
    return datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")


def save_note(text: str) -> str:
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(f"[{get_time()}] {text}\n")
    return "Note saved to notes.txt"


# Name -> function mapping (the model says a tool name, we run the matching function)
FUNCTIONS = {
    "get_weather": get_weather,
    "calculator": calculator,
    "get_time": get_time,
    "save_note": save_note,
}

# We must tell the model which tools exist and what inputs they need (JSON Schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the current (live) weather of a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name, e.g. Delhi"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Solves a math expression, e.g. '34 - 29' or '(120*3)/4'",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Returns the current date and time",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Saves a note or reminder for the user to a file",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        },
    },
]
