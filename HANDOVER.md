# Handover

> **Regel:** Am Ende jeder Session diese Datei aktualisieren. Altes entfernen, Neues ergänzen. Schlank halten — nur was die nächste Session braucht.

## Projektstatus

**VoiceTool** — macOS Voice-Dictation App (Hotkey → Sprechen → Text im aktiven Textfeld)

| Bereich | Status |
|---|---|
| Python-Backend | Alle Module implementiert, 29/29 Tests grün |
| Landing Page | `web/` — Next.js + Tailwind, Build erfolgreich |
| Git | Repo initialisiert, noch **kein erster Commit** |
| Manueller Test | Noch nicht durchgeführt |

## Erledigte Arbeit

### Python-Module (alle fertig + getestet)
- `audio.py` — AudioRecorder (sounddevice, threadsafe, start/stop)
- `transcribe.py` — Transcriber (mlx-whisper, whisper-small-mlx)
- `context.py` — get_active_app_name (pyobjc/NSWorkspace)
- `inject.py` — Accessibility API + Clipboard-Fallback (erkennt Electron-Apps)
- `postprocess.py` — Claude Haiku API, Fallback auf Rohtext bei Fehler
- `main.py` — Hotkey-Listener (pynput), orchestriert den Flow
- `tests/` — Unit Tests für alle Module (pytest + pytest-mock)

### Infrastruktur
- Python 3.12 via Homebrew, venv in `.venv/`
- `requirements.txt`, `.gitignore`, `config.yaml`, `config.example.yaml`
- Hotkey ist **F5** (fn nicht abfangbar via pynput)

### Landing Page (`web/`)
- Next.js 16 + Tailwind, Static Export (`output: "export"`)
- Sections: Hero, Features, How it works, Requirements, Footer
- Dunkles Design, blauer Akzent, macOS-Ästhetik

## Offene Aufgaben (nächste Session)

1. **Erster Commit** erstellen (alles stagen, sinnvolle Message)
2. **Manueller Test** der Python-App:
   - API-Key in `config.yaml` eintragen
   - macOS Permissions setzen (Mikrofon + Bedienungshilfen)
   - `python main.py` starten, F5 testen
   - Siehe Checkliste: `.claude/plans/keen-forging-eclipse.md`
3. **GitHub Repo** anlegen + pushen
4. **Landing Page** reviewen und ggf. anpassen
5. **Vercel Deploy** einrichten

## Entscheidungen

| Entscheidung | Gewählt | Grund |
|---|---|---|
| Hotkey | F5 | fn nicht abfangbar via pynput |
| Whisper-Modell | whisper-small-mlx | Schnelleres Prototyping |
| Python | 3.12 via Homebrew | System-Python war 3.9.6 |
| Frontend | Next.js + Tailwind | User-Wahl, Vercel-Deploy |
| Post-Processing | Claude Haiku 4.5 | Schnell + günstig |

## Dateistruktur

```
Voice app/
├── CLAUDE.md, RULES.md, SKILLS.md, AGENTS.md, SETUP.md
├── HANDOVER.md          ← diese Datei
├── main.py, audio.py, transcribe.py, context.py, inject.py, postprocess.py
├── config.yaml, config.example.yaml, requirements.txt
├── .gitignore, .venv/
├── tests/
│   ├── test_audio.py, test_transcribe.py, test_context.py
│   ├── test_inject.py, test_postprocess.py
└── web/                 ← Next.js Landing Page
    ├── app/page.tsx, app/layout.tsx, app/globals.css
    ├── next.config.ts
    └── package.json
```
