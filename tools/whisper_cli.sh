#!/bin/zsh
# CLI-Wrapper für OpenClaw media understanding (audio).
# Aufruf: whisper_cli.sh <MediaPath>
# Gibt nur den Transkript-Text auf stdout aus.
exec ~/.gcalcli-venv/bin/python ~/PA/tools/transcribe.py "$1" de 2>/dev/null
