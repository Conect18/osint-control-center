"""Interpretación estructurada de resultados OSINT."""

import contextlib
import json
import re
from pathlib import Path


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def parse_nmap(folder):
    folder = Path(folder)
    text = _read_text(folder / "scan.txt")

    result = {
        "tool": "Nmap",
        "host": None,
        "status": "Desconocido",
        "addresses": [],
        "latency": None,
        "ports": [],
        "filtered": 0,
        "duration": None,
        "evidence": "scan.txt",
    }

    match = re.search(
        r"^\s*\[(\+|-|x)\]\s*([A-Za-z0-9.-]+\.[A-Za-z]{2,})\s*$",
        text,
        re.MULTILINE,
    )

    if match:
        result["host"] = match.group(2)
        result["addresses"].append(match.group(2))

    match = re.search(r"Nmap scan report for (.+)", text)
    if match and not result["host"]:
        result["host"] = match.group(1).strip()

    result["status"] = (
        "Activo" if "Host is up" in text else "Sin respuesta"
    )

    match = re.search(r"Host is up \(([\d.]+)s latency\)", text)
    if match:
        result["latency"] = float(match.group(1))

    result["addresses"].extend(
        re.findall(
            r"Other addresses for .+?: ([0-9a-fA-F:.]+)",
            text,
        )
    )

    match = re.search(r"Not shown: (\d+) filtered tcp ports", text)
    if match:
        result["filtered"] = int(match.group(1))

    for line in text.splitlines():
        match = re.match(
            r"^\s*(\d+)/tcp\s+(\S+)\s+(\S+)(?:\s+(.*))?$",
            line,
        )
        if match:
            result["ports"].append({
                "port": int(match.group(1)),
                "state": match.group(2),
                "service": match.group(3),
                "version": (match.group(4) or "").strip(),
            })

    match = re.search(r"scanned in ([\d.]+) seconds", text)
    if match:
        result["duration"] = float(match.group(1))

    reverse = re.search(r"rDNS record for ([\d.]+): (.+)", text)
    if reverse:
        result["reverse_dns"] = reverse.group(2).strip()

    return result


def parse_sublist3r(folder):
    folder = Path(folder)

    subdomains = sorted({
        line.strip().lower()
        for line in _read_text(folder / "subdomains.txt").splitlines()
        if line.strip()
        and " " not in line.strip()
        and "." in line.strip()
    })

    return {
        "tool": "Sublist3r",
        "subdomains": subdomains,
        "total": len(subdomains),
        "evidence": "subdomains.txt",
    }


def parse_sherlock(folder):
    """Extrae perfiles y URL encontrados por Sherlock."""
    folder = Path(folder)
    text = _read_text(folder / "stdout.txt")

    profiles = []

    for line in text.splitlines():
        match = re.match(
            r"^\s*\[\+\]\s*(.+?):\s*(https?://\S+)",
            line,
        )
        if match:
            profiles.append({
                "site": match.group(1).strip(),
                "url": match.group(2).strip(),
            })

    summary = re.search(
        r"Search completed with (\d+) results",
        text,
    )

    return {
        "tool": "Sherlock",
        "profiles": profiles,
        "total": len(profiles),
        "reported_total": int(summary.group(1)) if summary else None,
        "evidence": "stdout.txt",
        "interpretation": (
            "Los perfiles encontrados son coincidencias potenciales. "
            "Es necesario verificar manualmente cada URL."
        ),
    }


def parse_holehe(folder):
    """Clasifica los resultados de comprobación de correo."""
    folder = Path(folder)
    text = _read_text(folder / "stdout.txt")

    used = []
    not_used = []
    rate_limited = []

    for line in text.splitlines():
        match = re.match(
            r"^\s*\[(\+|-|x)\]\s*([A-Za-z0-9.-]+\.[A-Za-z]{2,})\s*$",
            line,
            re.IGNORECASE,
        )

        if not match:
            continue

        marker = match.group(1).lower()
        site = match.group(2).strip()

        if marker == "+":
            used.append(site)
        elif marker == "-":
            not_used.append(site)
        else:
            rate_limited.append(site)

    return {
        "tool": "Holehe",
        "used": used,
        "not_used": not_used,
        "rate_limited": rate_limited,
        "total_used": len(used),
        "total_not_used": len(not_used),
        "total_rate_limited": len(rate_limited),
        "evidence": "stdout.txt",
        "interpretation": (
            "Los resultados indican respuestas de los servicios "
            "consultados; no demuestran por sí solos la titularidad "
            "del correo."
        ),
    }


def parse_maigret(folder):
    """Interpreta los informes JSON individuales de Maigret."""
    folder = Path(folder)

    profiles = []
    seen = set()

    for path in sorted(folder.glob("report_*_simple.json")):
        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            continue

        if not isinstance(data, dict):
            continue

        for site, entry in data.items():
            if not isinstance(entry, dict):
                continue

            status_data = entry.get("status", {})

            if isinstance(status_data, dict):
                status = status_data.get("status", "Unknown")
                username = status_data.get(
                    "username",
                    entry.get("username", ""),
                )
                url = (
                    status_data.get("url")
                    or entry.get("url_user")
                    or entry.get("url_main")
                )
            else:
                status = str(status_data)
                username = entry.get("username", "")
                url = entry.get("url_user") or entry.get("url_main")

            profile = {
                "site": site,
                "username": username,
                "status": status,
                "url": url,
            }

            key = (
                site.lower(),
                str(username).lower(),
                str(status).lower(),
                str(url).lower(),
            )

            if key not in seen:
                seen.add(key)
                profiles.append(profile)

    claimed = [
        profile for profile in profiles
        if profile["status"].lower() == "claimed"
    ]

    other = [
        profile for profile in profiles
        if profile["status"].lower() != "claimed"
    ]

    return {
        "tool": "Maigret",
        "profiles": profiles,
        "claimed": claimed,
        "other": other,
        "total": len(profiles),
        "total_claimed": len(claimed),
        "total_other": len(other),
        "evidence": "report_*_simple.json",
        "interpretation": (
            "Los resultados Claimed indican perfiles que Maigret "
            "considera registrados. Deben verificarse manualmente "
            "para descartar coincidencias incorrectas."
        ),
    }


def parse_execution(path):
    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return {}


def parse_case(case_dir):
    """Interpreta los resultados disponibles de un caso."""

    case_dir = Path(case_dir)
    info = {}

    with contextlib.suppress(OSError, json.JSONDecodeError):
        info = json.loads(
            (case_dir / "info.json").read_text(encoding="utf-8")
        )

    report = {
        "case_id": info.get("case_id", case_dir.name),
        "target": info.get("target", "Desconocido"),
        "type": info.get("type", "Desconocido"),
        "status": info.get("status", "Desconocido"),
        "tools": [],
    }

    for execution_file in sorted(
        case_dir.glob("*/*/execution.json")
    ):
        metadata = parse_execution(execution_file)
        tool = metadata.get("tool", "").lower()
        folder = execution_file.parent

        item = {
            "tool": metadata.get("tool", "Desconocida"),
            "status": metadata.get("status", "unknown"),
            "findings": metadata.get("findings", 0),
            "duration": metadata.get("duration", 0),
            "evidence": str(execution_file.relative_to(case_dir)),
        }

        if tool == "nmap":
            item["analysis"] = parse_nmap(folder)

        elif tool == "sublist3r":
            item["analysis"] = parse_sublist3r(folder)

        elif tool == "sherlock":
            item["analysis"] = parse_sherlock(folder)

        elif tool == "holehe":
            item["analysis"] = parse_holehe(folder)

        elif tool == "maigret":
            item["analysis"] = parse_maigret(folder)

        report["tools"].append(item)

    return report
