"""Normalización y validación de objetivos.

Todo lo que entra al runner pasa por aquí. Devuelve el valor limpio o lanza
InvalidTarget con un motivo legible; nunca devuelve algo a medias.
"""

import ipaddress
import re

LABEL = re.compile(r"^(?!-)[a-z0-9-]{1,63}(?<!-)$")
TLD = re.compile(r"^[a-z]{2,63}$")
USER = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
EMAIL = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}$")
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

MAX_DOMAIN = 253
MAX_USER = 64
MAX_EMAIL = 254
MAX_SLUG = 60


class InvalidTarget(ValueError):
    """Objetivo que no supera la validación."""


def _clean(raw):
    if raw is None:
        raise InvalidTarget("vacío")
    value = raw.strip()
    if not value:
        raise InvalidTarget("vacío")
    if any(c.isspace() for c in value):
        raise InvalidTarget("contiene espacios")
    return value


def normalize_domain(raw):
    """Devuelve el dominio canónico: minúsculas, sin esquema, sin www, sin puerto."""
    value = _clean(raw).lower()

    if "://" in value:
        value = value.split("://", 1)[1]
    value = value.split("/", 1)[0]
    value = value.split("?", 1)[0]
    value = value.split("#", 1)[0]

    if "@" in value:
        value = value.rsplit("@", 1)[1]

    if value.count(":") == 1:
        host, port = value.split(":", 1)
        if port.isdigit():
            value = host

    value = value.rstrip(".")
    if not value:
        raise InvalidTarget("vacío")
    if value.startswith("www."):
        value = value[4:]

    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        pass

    if len(value) > MAX_DOMAIN:
        raise InvalidTarget("dominio demasiado largo")

    labels = value.split(".")
    if len(labels) < 2:
        raise InvalidTarget("sin TLD")
    if not TLD.match(labels[-1]):
        raise InvalidTarget("TLD inválido")
    for label in labels:
        if not LABEL.match(label):
            raise InvalidTarget(f"etiqueta inválida: {label!r}")

    return value


def normalize_ip(raw):
    value = _clean(raw)
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        raise InvalidTarget("IP inválida") from None


def normalize_user(raw):
    value = _clean(raw).lstrip("@").lower()
    if not value:
        raise InvalidTarget("vacío")
    if len(value) > MAX_USER:
        raise InvalidTarget("usuario demasiado largo")
    if not USER.match(value):
        raise InvalidTarget("caracteres no permitidos")
    return value


def normalize_email(raw):
    value = _clean(raw).lower()
    if len(value) > MAX_EMAIL:
        raise InvalidTarget("email demasiado largo")
    if not EMAIL.match(value):
        raise InvalidTarget("formato de email inválido")
    return value


def slugify(text, fallback="sin-nombre"):
    """Convierte texto libre en un nombre seguro para directorios."""
    value = ANSI.sub("", str(text or "")).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:MAX_SLUG] or fallback


def strip_ansi(text):
    return ANSI.sub("", text or "")


_KIND = {
    "users": normalize_user, "username": normalize_user, "user": normalize_user,
    "emails": normalize_email, "email": normalize_email,
    "domains": normalize_domain, "domain": normalize_domain,
    "hosts": normalize_domain, "host": normalize_domain,
    "ips": normalize_ip, "ip": normalize_ip,
}


def normalize_target(kind, raw):
    """Normaliza según la categoría; rechaza categorías desconocidas."""
    try:
        fn = _KIND[kind]
    except KeyError:
        raise InvalidTarget(f"categoría desconocida: {kind}") from None
    return fn(raw)
