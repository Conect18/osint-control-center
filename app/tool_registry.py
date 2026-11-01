"""Registro central de herramientas OSINT con estado persistente."""

import json
from pathlib import Path

from app.services import (
    holehe_service, maigret_service, nmap_service, sherlock_service, sublist3r_service,
)

STATE_FILE = Path(__file__).resolve().parent / "config" / "tools.json"

TOOLS = {
    "users": [
        {"name": "Sherlock", "runner": sherlock_service.run},
        {"name": "Maigret", "runner": maigret_service.run},
    ],
    "emails": [{"name": "Holehe", "runner": holehe_service.run}],
    "domains": [
        {"name": "Sublist3r", "runner": sublist3r_service.run},
        {"name": "Nmap", "runner": nmap_service.run},
    ],
    "hosts": [{"name": "Nmap", "runner": nmap_service.run}],
    "phones": [],
    "images": [],
}


def _load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def is_enabled(category, name):
    return _load_state().get(category, {}).get(name, True)


def get_tools(category):
    return [t for t in TOOLS.get(category, []) if is_enabled(category, t["name"])]


def set_enabled(category, name, enabled: bool):
    state = _load_state()
    state.setdefault(category, {})[name] = enabled
    _save_state(state)


def enable_tool(category, name):
    set_enabled(category, name, True)


def disable_tool(category, name):
    set_enabled(category, name, False)
