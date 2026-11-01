#!/bin/bash
set -uo pipefail

echo "==============================="
echo "      OSINT LAB CHECK"
echo "==============================="

echo; echo "[Sistema]"; uname -a
echo; echo "[Python]"; python3 --version

echo; echo "[Git]"
if command -v git >/dev/null 2>&1; then git --version; else echo "✘ git"; fi

echo; echo "[Herramientas OSINT]"
for tool in sherlock holehe maigret sublist3r nmap; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✔ $tool"
    else
        echo "✘ $tool"
    fi
done

echo; echo "[Espacio]"; df -h /
