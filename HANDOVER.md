# Handover

> **Regel:** Am Ende jeder Session diese Datei aktualisieren. Altes entfernen, Neues ergänzen. Schlank halten — nur was die nächste Session braucht.

## Projektstatus

**VoiceTool** — macOS Voice-Dictation App (Hotkey → Sprechen → Text im aktiven Textfeld)

| Bereich | Status |
|---|---|
| Python-Backend | Alle Module implementiert, manuell getestet, funktioniert |
| Landing Page | `web/` — Next.js + Tailwind, Build erfolgreich |
| Git | Initial Commit + Bugfixes committed |
| GitHub | **https://github.com/sahinelcoder/VoiceTool** (public) |
| Manueller Test | Erfolgreich — Recording, Transkription, Claude API, Clipboard-Injection funktionieren |

## Was diese Session erledigt wurde

- **Initial Commit** erstellt und auf GitHub gepusht
- **GitHub CLI** (`gh`) installiert und Repo angelegt
- **Bugfix `main.py`**: `pynput`-Import war falsch platziert → `UnboundLocalError` behoben
- **Bugfix `inject.py`**: Accessibility API nutzte falsche ObjC-Methoden → auf C-Funktionen (`AXUIElementCopyAttributeValue`/`AXUIElementSetAttributeValue`) umgestellt
- **Bugfix `config.yaml`**: Zeilenumbruch im API-Key entfernt
- **Manueller Test** erfolgreich: Voller Flow (F5 → Recording → Transkription 0.57s → Claude API Post-Processing → Clipboard-Injection)
- **macOS Permissions** gesetzt (Mikrofon + Bedienungshilfen)

## Offene Aufgaben (nächste Session)

1. **Hotkey ändern**: F5 ist unpraktisch → **Pfeiltaste Links + Rechts gleichzeitig** als neuer Hotkey
   - `main.py`: `_key_matches` und Listener-Logik anpassen für Combo-Key
   - `config.yaml` / `config.example.yaml` aktualisieren
2. **Recording-Animation**: Visuelles Feedback während Aufnahme läuft
   - Progressbar/Overlay auf dem Bildschirm anzeigen solange aufgenommen wird
   - Vermutlich pyobjc/AppKit NSWindow als transparentes Overlay
3. **Accessibility-Injection testen** — Permissions wurden erteilt, aber noch nicht verifiziert ob es jetzt ohne Clipboard-Fallback klappt
4. **Landing Page** reviewen und ggf. anpassen
5. **Vercel Deploy** einrichten
6. **Bugfix-Commit** erstellen und pushen (main.py, inject.py Fixes noch uncommitted)

## Entscheidungen

| Entscheidung | Gewählt | Grund |
|---|---|---|
| Hotkey | F5 (wird geändert) | fn nicht abfangbar via pynput, F5 unpraktisch |
| Neuer Hotkey | Pfeiltaste Links + Rechts | User-Wahl, ergonomischer |
| Whisper-Modell | whisper-small-mlx | Schnelleres Prototyping |
| Python | 3.12 via Homebrew | System-Python war 3.9.6 |
| Frontend | Next.js + Tailwind | User-Wahl, Vercel-Deploy |
| Post-Processing | Claude Haiku 4.5 | Schnell + günstig |
| Text-Injection | Clipboard-Fallback als Default | Accessibility API instabil bei manchen Apps |

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
