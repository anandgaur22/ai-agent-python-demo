"""
config.py - Decides which LLM (model) the project uses.

All three options are FREE:
  1. ollama -> A local model running on your laptop (no internet or API key needed)
  2. gemini -> Google AI Studio free API key (aistudio.google.com)
  3. groq   -> Groq free API key (console.groq.com), very fast

All three offer an "OpenAI-compatible" API, so the code stays the same.
Only the base_url, api_key and model name change.
"""
import os
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()          # Load settings from the .env file
except ImportError:
    pass

PROVIDER = os.getenv("PROVIDER", "ollama").lower()

PROVIDERS = {
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",                                   # dummy value, Ollama does not need a key
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key": os.getenv("GEMINI_API_KEY"),
        "model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": os.getenv("GROQ_API_KEY"),
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    },
}

if PROVIDER not in PROVIDERS:
    raise SystemExit(f"Invalid PROVIDER '{PROVIDER}'. Use one of: ollama | gemini | groq")

_cfg = PROVIDERS[PROVIDER]
if not _cfg["api_key"]:
    raise SystemExit(f"{PROVIDER.upper()}_API_KEY is missing. Add it to your .env file.")

client = OpenAI(base_url=_cfg["base_url"], api_key=_cfg["api_key"])
MODEL = _cfg["model"]

print(f"[Config] Provider: {PROVIDER} | Model: {MODEL}")
