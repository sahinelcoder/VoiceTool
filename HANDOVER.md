# Handover

> **Regel:** Am Ende jeder Session diese Datei aktualisieren. Altes entfernen, Neues ergänzen. Schlank halten — nur was die nächste Session braucht.

## Projektstatus

**VoiceTool** — macOS Voice-Dictation App (Hotkey → Sprechen → Text im aktiven Textfeld)

| Bereich | Status |
|---|---|
| Python-Backend | Alle Module implementiert, funktioniert |
| Waveform-Overlay | Audio-reaktive Bars über dem Dock, funktioniert |
| Menu Bar Icon | 🎙 idle / 🔴 recording, Dropdown mit Status + Beenden |
| App Bundle | VoiceTool.app via PyInstaller gebaut (555 MB), funktioniert |
| Hotkey | Fn/Globe (🌐) via Quartz CGEventTap |
| Text-Injection | Fix: `kAXSelectedTextAttribute` statt `kAXValueAttribute` — überschreibt nicht mehr |
| Post-Processing | Behält Umgangssprache bei, nur Satzzeichen + Whisper-Fehler |
| Landing Page | `web/` — Next.js + Tailwind, live auf Vercel |
| Chrome / Browser | Text-Injection via Clipboard-Fallback, funktioniert |
| Terminal-Emulatoren | Text-Injection via Clipboard-Fallback, funktioniert |
| Git | Alles committed + gepusht |
| GitHub | **https://github.com/sahinelcoder/VoiceTool** (public) |
| Vercel | **https://voicetool-app.vercel.app** |

## Was diese Session erledigt wurde

- **Chrome-Bug bestätigt behoben** — war bereits in `CLIPBOARD_FALLBACK_APPS`, funktioniert
- **Terminal-Injection gefixt** — Terminal-Emulatoren zu `CLIPBOARD_FALLBACK_APPS` hinzugefügt
- **Clipboard-Delay erhöht** — 0.1s → 0.5s, damit Chrome/Browser Cmd+V verarbeiten können bevor Clipboard wiederhergestellt wird

## Offene Aufgaben (nächste Session)

1. **Desktop-App mit Settings-GUI bauen** — Features mit User klären:
   - **Dictionary** (eigene Wörter, z.B. Name "Sahin", Slang) → wird an Post-Processing-Prompt übergeben
   - **Snippets** (Kürzel → Text-Expansion, z.B. "@@email" → "sahin@example.com")
   - **General Settings**: Hotkey-Auswahl, Sprache, Post-Processing an/aus, Modell-Auswahl
   - **Was noch?** → User zu Beginn der nächsten Session fragen
2. **Whisper-Modell testen** — `whisper-large-v3-mlx-4bit` prüfen (Genauigkeit vs. RAM)

## Entscheidungen

| Entscheidung | Gewählt | Grund |
|---|---|---|
| Hotkey | Fn/Globe (🌐) | User-Wahl, ergonomischer. Quartz CGEventTap nötig (pynput kann Fn nicht) |
| Whisper-Modell | whisper-large-v3-mlx-4bit | Beste Genauigkeit bei ~800 MB RAM |
| Sprache | `de` (explizit) | Auto-Detection unzuverlässig bei kurzen Sätzen |
| Python | 3.12 via Homebrew | System-Python war 3.9.6 |
| Frontend | Next.js + Tailwind | User-Wahl, Vercel-Deploy |
| Post-Processing | Claude Haiku 4.5, nur Satzzeichen | Umgangssprache beibehalten, nicht "verbessern" |
| Text-Injection | `kAXSelectedTextAttribute` | Fügt am Cursor ein, überschreibt nicht. Clipboard-Fallback für Electron-Apps |
| Overlay | NSTimer + shared variable | callAfter-Chain war unzuverlässig für Audio-Level-Updates |
| App Bundle | PyInstaller | py2app hatte RecursionError mit mlx-Packages |
| Menu Bar | `LSUIElement=True` + `setActivationPolicy_(1)` | Kein Dock-Icon, nur Menu Bar |
| Vercel URL | voicetool-app.vercel.app | voicetool.vercel.app war vergeben |

## Dateistruktur

```
Voice app/
├── CLAUDE.md, RULES.md, SKILLS.md, AGENTS.md, SETUP.md
├── HANDOVER.md          ← diese Datei
├── README.md
├── main.py              ← + Menu Bar Icon, Fn-Key-Listener
├── audio.py, transcribe.py, context.py, postprocess.py
├── inject.py            ← Fix: kAXSelectedTextAttribute
├── overlay.py           ← Waveform-Overlay
├── setup.py             ← py2app (nicht genutzt, PyInstaller stattdessen)
├── VoiceTool.spec       ← PyInstaller Build-Config
├── config.yaml, config.example.yaml, requirements.txt
├── .gitignore, .venv/
├── dist/                ← VoiceTool.app (gitignored)
├── build/               ← PyInstaller build artifacts (gitignored)
├── tests/
│   ├── test_audio.py, test_transcribe.py, test_context.py
│   ├── test_inject.py, test_postprocess.py
└── web/                 ← Next.js Landing Page (Vercel)
    ├── app/page.tsx, app/layout.tsx, app/globals.css
    ├── next.config.ts
    └── package.json
```
