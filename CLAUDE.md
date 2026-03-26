# VoiceTool

Voice-dictation app für macOS Apple Silicon. Hotkey halten → sprechen → loslassen → bereinigter Text erscheint im aktiven Textfeld.

## Stack

| Schicht | Tool |
|---|---|
| Transkription | `mlx-whisper` (läuft auf Neural Engine) |
| Audio | `sounddevice` + `numpy` |
| Hotkey | `pynput` |
| App-Kontext | `pyobjc` + `AppKit` |
| Post-Processing | Claude API Haiku |
| Text-Injection | `pyobjc` Accessibility API + Clipboard-Fallback |
| Config | `config.yaml` |

## Projektstruktur

```
voicetool/
├── CLAUDE.md         ← diese Datei (Kontext für Claude Code)
├── RULES.md          ← Coding Standards
├── SKILLS.md         ← Review & Testing Skills
├── AGENTS.md         ← Sub-Agent Definitionen
├── main.py           ← Einstiegspunkt, Hotkey-Listener
├── audio.py          ← Mikrofon-Recording
├── transcribe.py     ← mlx-whisper Integration
├── context.py        ← Aktives Fenster auslesen
├── postprocess.py    ← Claude API Cleanup
├── inject.py         ← Text-Injection + Fallback
├── config.yaml       ← Einstellungen
└── requirements.txt
```

## Datenfluss

```
Hotkey gedrückt → Audio aufnehmen → Hotkey losgelassen
→ mlx-whisper → Rohtext
→ App-Name auslesen (pyobjc)
→ Claude Haiku API (Rohtext + App-Name) → bereinigter Text
→ Text in aktives Textfeld injizieren
```

## Latenz-Ziel

Unter 1.5 Sekunden gesamt auf M3.

## Wichtige Constraints

- Kein Screenshot, kein Cloud-Upload von Audio
- Kein Auto-Start ohne User-Erlaubnis
- RAM-Verbrauch im Idle unter 100 MB
- Kein Recording-Limit
- Clipboard-Fallback für Electron-Apps (Slack, VS Code, Notion)

## Build-Reihenfolge

1. `audio.py`
2. `transcribe.py`
3. `context.py`
4. `inject.py`
5. `postprocess.py`
6. `main.py`

## Benötigte macOS-Permissions

- Mikrofon
- Bedienungshilfen (Accessibility) — für Text-Injection zwingend
