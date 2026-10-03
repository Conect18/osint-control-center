#!/bin/bash

# ===== VALIDACIÓN =====
if [ -z "$1" ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

USER="$1"
DATE=$(date +%Y-%m-%d)
BASE="$HOME/osint-lab/results/$USER"
LOG="$BASE/scan.log"

# ===== SETUP =====
mkdir -p "$BASE/maigret"
mkdir -p "$BASE/sherlock"

# Crear log desde el inicio
touch "$LOG"

echo "==============================" | tee -a "$LOG"
echo " OSINT Scan Started" | tee -a "$LOG"
echo " Target: $USER" | tee -a "$LOG"
echo " Date: $DATE" | tee -a "$LOG"
echo "==============================" | tee -a "$LOG"

# ===== CHECK TOOLS =====
if ! command -v maigret >/dev/null 2>&1; then
    echo "[ERROR] Maigret not installed" | tee -a "$LOG"
    exit 1
fi

if ! command -v sherlock >/dev/null 2>&1; then
    echo "[ERROR] Sherlock not installed" | tee -a "$LOG"
    exit 1
fi

# ===== MAIGRET =====
echo "" | tee -a "$LOG"
echo "[1] Running Maigret..." | tee -a "$LOG"

maigret "$USER" --timeout 10 --folderoutput "$BASE/maigret" >> "$LOG" 2>&1

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "[OK] Maigret completed" | tee -a "$LOG"
else
    echo "[ERROR] Maigret failed" | tee -a "$LOG"
fi

# ===== SHERLOCK =====
echo "" | tee -a "$LOG"
echo "[2] Running Sherlock..." | tee -a "$LOG"

sherlock "$USER" --output "$BASE/sherlock/sherlock.txt" >> "$LOG" 2>&1

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "[OK] Sherlock completed" | tee -a "$LOG"
else
    echo "[ERROR] Sherlock failed" | tee -a "$LOG"
fi

# ===== FIN =====
echo "" | tee -a "$LOG"
echo "Scan finished." | tee -a "$LOG"
echo "Results saved in: $BASE" | tee -a "$LOG"
