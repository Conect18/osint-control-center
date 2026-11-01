import pytest

from app.core.normalize import (
    InvalidTarget,
    normalize_domain,
    normalize_email,
    normalize_ip,
    normalize_user,
    slugify,
    strip_ansi,
)


@pytest.mark.parametrize(
    "raw, esperado",
    [
        ("www.google.com", "google.com"),
        ("https://www.google.com/", "google.com"),
        ("http://google.com:8080/buscar?q=1", "google.com"),
        ("  Google.COM.  ", "google.com"),
        ("user@correo.com@dominio.com", "dominio.com"),
        ("google.com#frag", "google.com"),
        ("8.8.8.8", "8.8.8.8"),
    ],
)
def test_domain_valido(raw, esperado):
    assert normalize_domain(raw) == esperado


@pytest.mark.parametrize(
    "raw",
    ["", "   ", "localhost", "google", "http://", "-mal.com", "mal-.com", "a b.com", "google.c"],
)
def test_domain_invalido(raw):
    with pytest.raises(InvalidTarget):
        normalize_domain(raw)


def test_user_limpia_arroba():
    assert normalize_user("@PabloG") == "pablog"


@pytest.mark.parametrize("raw", ["", "a b", "usuario!", "x" * 65])
def test_user_invalido(raw):
    with pytest.raises(InvalidTarget):
        normalize_user(raw)


def test_email_valido():
    assert normalize_email(" DataCenterUYk28@Gmail.com ") == "datacenteruyk28@gmail.com"


@pytest.mark.parametrize("raw", ["", "sin-arroba.com", "a@b", "a@@b.com"])
def test_email_invalido(raw):
    with pytest.raises(InvalidTarget):
        normalize_email(raw)


def test_ip():
    assert normalize_ip(" 8.8.8.8 ") == "8.8.8.8"
    with pytest.raises(InvalidTarget):
        normalize_ip("999.1.1.1")


def test_strip_ansi():
    assert strip_ansi("\x1b[32mOK\x1b[0m") == "OK"


def test_slugify():
    assert slugify("CASE 2026/10/30") == "case-2026-10-30"
    assert slugify("") == "sin-nombre"
