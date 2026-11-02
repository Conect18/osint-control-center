import json

from app.core.result_parser import (
    parse_case,
    parse_execution,
    parse_holehe,
    parse_maigret,
    parse_nmap,
    parse_sherlock,
    parse_sublist3r,
)


def test_parse_nmap_extrae_host_y_puertos(tmp_path):
    (tmp_path / "scan.txt").write_text(
        "[+] ejemplo.com\n"
        "Host is up (0.025s latency).\n"
        "22/tcp open ssh OpenSSH\n"
        "80/tcp open http Apache\n"
        "Nmap done: scanned in 2.5 seconds\n",
        encoding="utf-8",
    )

    result = parse_nmap(tmp_path)

    assert result["host"] == "ejemplo.com"
    assert result["addresses"] == ["ejemplo.com"]
    assert result["status"] == "Activo"
    assert result["latency"] == 0.025
    assert len(result["ports"]) == 2
    assert result["ports"][0]["port"] == 22
    assert result["duration"] == 2.5


def test_parse_sublist3r_elimina_duplicados(tmp_path):
    (tmp_path / "subdomains.txt").write_text(
        "mail.ejemplo.com\n"
        "www.ejemplo.com\n"
        "mail.ejemplo.com\n",
        encoding="utf-8",
    )

    result = parse_sublist3r(tmp_path)

    assert result["total"] == 2
    assert result["subdomains"] == [
        "mail.ejemplo.com",
        "www.ejemplo.com",
    ]


def test_parse_sherlock_extrae_perfiles(tmp_path):
    (tmp_path / "stdout.txt").write_text(
        "[+] GitHub: https://github.com/objetivo\n"
        "[+] Reddit: https://reddit.com/u/objetivo\n",
        encoding="utf-8",
    )

    result = parse_sherlock(tmp_path)

    assert result["total"] == 2
    assert result["profiles"][0]["site"] == "GitHub"


def test_parse_holehe_clasifica_resultados(tmp_path):
    (tmp_path / "stdout.txt").write_text(
        "[+] github.com\n"
        "[-] reddit.com\n"
        "[x] example.com\n",
        encoding="utf-8",
    )

    result = parse_holehe(tmp_path)

    assert result["total_used"] == 1
    assert result["total_not_used"] == 1
    assert result["total_rate_limited"] == 1


def test_parse_maigret_clasifica_perfiles(tmp_path):
    data = {
        "GitHub": {
            "status": {
                "status": "Claimed",
                "username": "objetivo",
                "url": "https://github.com/objetivo",
            }
        },
        "Reddit": {
            "status": {
                "status": "Available",
                "username": "objetivo",
                "url": "https://reddit.com/u/objetivo",
            }
        },
    }

    (tmp_path / "report_objetivo_simple.json").write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    result = parse_maigret(tmp_path)

    assert result["total"] == 2
    assert result["total_claimed"] == 1
    assert result["total_other"] == 1


def test_parse_execution_json_invalido(tmp_path):
    path = tmp_path / "execution.json"
    path.write_text("{json invalido", encoding="utf-8")

    assert parse_execution(path) == {}


def test_parse_case_sin_herramientas(tmp_path):
    (tmp_path / "info.json").write_text(
        json.dumps({
            "case_id": "CASE-TEST",
            "target": "ejemplo.com",
            "type": "domain",
            "status": "active",
        }),
        encoding="utf-8",
    )

    result = parse_case(tmp_path)

    assert result["case_id"] == "CASE-TEST"
    assert result["target"] == "ejemplo.com"
    assert result["tools"] == []
