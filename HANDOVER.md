# Handover

> **Regel:** Am Ende jeder Session diese Datei aktualisieren. Altes entfernen, Neues ergänzen. Schlank halten — nur was die nächste Session braucht.

## Projektstatus

**VoiceTool** — macOS Voice-Dictation App (Hotkey → Sprechen → Text im aktiven Textfeld)

| Bereich | Status |
|---|---|
| Python-Backend | Alle Module implementiert, manuell getestet, funktioniert |
| Recording-Overlay | Dunkle Pill mit pulsierendem roten Dot, funktioniert |
| Landing Page | `web/` — Next.js + Tailwind, live auf Vercel |
| Git | Alles committed + gepusht |
| GitHub | **https://github.com/sahinelcoder/VoiceTool** (public) |
| Vercel | **https://web-nine-sandy-68.vercel.app** (live) |
| Manueller Test | Erfolgreich — voller Flow funktioniert inkl. Overlay |

## Was diese Session erledigt wurde

- **Bugfix-Commit**: pynput Import + AXUIElement C-Funktionen gefixt
- **Hotkey umgebaut**: F5 → Pfeiltaste Links + Rechts gleichzeitig (`arrow_combo`)
- **Recording-Overlay**: `overlay.py` — dunkle Pill mit pulsierendem roten Dot oben-mittig
- **Overlay-Fix**: AppKit Event Loop auf Main Thread, pynput Listener im Background
- **Landing Page**: GitHub-Links auf echtes Repo gefixt, Hotkey-Beschreibung aktualisiert
- **Vercel Deploy**: Landing Page live geschaltet
- **Whisper-Modell**: Upgrade auf `whisper-large-v3-mlx-4bit` + Sprache auf `de` gesetzt (bessere Genauigkeit, ~800 MB RAM)
- **Alle Commits gepusht** auf GitHub

## Offene Aufgaben (nächste Session)

1. **Overlay testen** — verifizieren dass die Pill beim Recording sichtbar ist
2. **Whisper-Modell testen** — prüfen ob 4-bit quantisiert korrekt läuft und Genauigkeit besser ist
3. **Accessibility-Injection testen** — in TextEdit/Notes diktieren, prüfen ob es ohne Clipboard-Fallback klappt
4. **Vercel URL** — umbenennen auf `voicetool.vercel.app` oder Custom Domain
5. **README.md** für GitHub-Repo erstellen
6. **App als .app Bundle** verpacken (optional, damit man es wie eine normale Mac-App starten kann)

## Entscheidungen

| Entscheidung | Gewählt | Grund |
|---|---|---|
| Hotkey | Pfeiltaste Links + Rechts gleichzeitig | User-Wahl, ergonomischer als F5 |
| Whisper-Modell | whisper-large-v3-mlx-4bit | Beste Genauigkeit bei ~800 MB RAM |
| Sprache | `de` (explizit) | Auto-Detection unzuverlässig bei kurzen Sätzen |
| Python | 3.12 via Homebrew | System-Python war 3.9.6 |
| Frontend | Next.js + Tailwind | User-Wahl, Vercel-Deploy |
| Post-Processing | Claude Haiku 4.5 | Schnell + günstig |
| Text-Injection | Clipboard-Fallback als Default | Accessibility API instabil bei manchen Apps |
| Overlay | AppKit NSWindow + Main Thread Event Loop | pyobjc braucht AppKit Run Loop für Fenster |

## Dateistruktur

```
Voice app/
├── CLAUDE.md, RULES.md, SKILLS.md, AGENTS.md, SETUP.md
├── HANDOVER.md          ← diese Datei
├── main.py, audio.py, transcribe.py, context.py, inject.py, postprocess.py
├── overlay.py           ← NEU: Recording-Overlay
├── config.yaml, config.example.yaml, requirements.txt
├── .gitignore, .venv/
├── tests/
│   ├── test_audio.py, test_transcribe.py, test_context.py
│   ├── test_inject.py, test_postprocess.py
└── web/                 ← Next.js Landing Page (Vercel)
    ├── app/page.tsx, app/layout.tsx, app/globals.css
    ├── next.config.ts
    └── package.json
```
