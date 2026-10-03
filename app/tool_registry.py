"""
Registro central de herramientas OSINT.
"""

from services.sherlock_service import run as sherlock
from services.maigret_service import run as maigret
from services.holehe_service import run as holehe
from services.sublist3r_service import run as sublist3r


TOOLS = {

    "users": [

        {
            "name": "Sherlock",
            "runner": sherlock,
            "enabled": True,
        },

        {
            "name": "Maigret",
            "runner": maigret,
            "enabled": True,
        }

    ],

    "emails": [

        {
            "name": "Holehe",
            "runner": holehe,
            "enabled": True,
        }

    ],

    "domains": [

        {
            "name": "Sublist3r",
            "runner": sublist3r,
            "enabled": True,
        }

    ],

    "phones": [

    ],

    "images": [

    ]

}


def get_tools(category):

    return [
        tool
        for tool in TOOLS.get(category, [])
        if tool["enabled"]
    ]


def enable_tool(category, name):

    for tool in TOOLS.get(category, []):

        if tool["name"] == name:
            tool["enabled"] = True


def disable_tool(category, name):

    for tool in TOOLS.get(category, []):

        if tool["name"] == name:
            tool["enabled"] = False
