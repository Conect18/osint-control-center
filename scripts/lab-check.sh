#!/bin/bash

echo "==============================="
echo "      OSINT LAB CHECK"
echo "==============================="

echo
echo "[Sistema]"
uname -a

echo
echo "[Python]"
python3 --version

echo
echo "[Git]"
git --version

echo
echo "[Node]"
node --version

echo
echo "[Nmap]"
nmap --version | head -1

echo
echo "[Herramientas OSINT]"
for tool in sherlock holehe maigret sublist3r; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✔ $tool"
    else
        echo "✘ $tool"
    fi
done

echo
echo "[Espacio]"
df -h /
