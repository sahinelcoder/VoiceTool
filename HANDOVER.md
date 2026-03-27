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
| Git | **Nicht committed** — alle Änderungen dieser + letzter Session |
| GitHub | **https://github.com/sahinelcoder/VoiceTool** (public) |
| Vercel | **https://voicetool-app.vercel.app** |

## Was diese Session erledigt wurde

- **Menu Bar Icon**: `NSStatusItem` oben rechts, wechselt zwischen 🎙 (idle) und 🔴 (recording), Dropdown-Menü mit Status + Beenden (⌘Q), `setActivationPolicy_(1)` für Dock-freie App
- **App Bundle**: PyInstaller `.app` Bundle (py2app hatte RecursionError mit mlx), `VoiceTool.spec` + `setup.py`, `LSUIElement=True` für Menu-Bar-only
- **Text-Injection Fix**: `kAXSelectedTextAttribute` statt `kAXValueAttribute` — Text wird am Cursor eingefügt, bestehender Inhalt bleibt erhalten
- **Hotkey auf Fn**: Quartz `CGEventTap` für `kCGEventFlagsChanged` mit `kCGEventFlagMaskSecondaryFn`, da pynput die Fn-Taste nicht erkennt

## Offene Aufgaben (nächste Session)

1. **Änderungen committen + pushen** — alles seit letzter Session (Menu Bar, App Bundle, Injection Fix, Fn-Hotkey, Overlay, Post-Processing, README)
2. **Bug: Text-Injection funktioniert nicht in Google Chrome** — Aufnahme + Transkription laufen, aber Text erscheint nicht im Browser-Textfeld. Native Apps (Notizen etc.) funktionieren. Vermutlich: Accessibility API (`kAXSelectedTextAttribute`) greift nicht bei Chrome-Textfeldern → Chrome evtl. in `ELECTRON_APPS` Set aufnehmen oder Clipboard-Fallback erzwingen. Muss debuggt werden.
3. **Desktop-App mit Settings-GUI bauen** — User explizit nach gewünschten Features fragen:
   - **Dictionary** (eigene Wörter, z.B. Name "Sahin", Slang) → wird an Post-Processing-Prompt übergeben
   - **Snippets** (Kürzel → Text-Expansion, z.B. "@@email" → "sahin@example.com")
   - **Was noch?** → User in nächster Session fragen, was alles rein soll (General Settings, Hotkey-Auswahl, Sprache, etc.)
3. **Whisper-Modell testen** — 4-bit quantisiert prüfen

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
