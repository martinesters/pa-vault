#!/usr/bin/env python3
"""Lokale Transkription (faster-whisper). Nutzung: transcribe.py <audio/video> [sprache]
Modell wird beim ersten Lauf geladen/gecacht. Default-Sprache: de."""
import sys, os
from faster_whisper import WhisperModel

path = os.path.expanduser(sys.argv[1])
lang = sys.argv[2] if len(sys.argv) > 2 else "de"
model_size = os.environ.get("WHISPER_MODEL", "small")

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe(path, language=lang, vad_filter=True)
out = " ".join(s.text.strip() for s in segments).strip()
print(out if out else "(kein Sprachinhalt erkannt)")
