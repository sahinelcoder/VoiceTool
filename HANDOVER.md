# Handover

> **Regel:** Am Ende jeder Session diese Datei aktualisieren. Altes entfernen, Neues ergänzen. Schlank halten — nur was die nächste Session braucht.

## Projektstatus

**VoiceTool** — macOS Voice-Dictation App (Hotkey → Sprechen → Text im aktiven Textfeld)

| Bereich | Status |
|---|---|
| Python-Backend | Alle Module implementiert, funktioniert |
| Streaming-Transkription | ✅ Neu: Chunks alle 30s im Hintergrund, 2s Overlap |
| Waveform-Overlay | Audio-reaktive Bars über dem Dock |
| Menu Bar Icon | 🎙 idle / 🔴 recording, Dropdown mit Status + Beenden |
| App Bundle | VoiceTool.app via PyInstaller (555 MB) |
| Hotkey | Fn/Globe (🌐) via Quartz CGEventTap |
| Text-Injection | `kAXSelectedTextAttribute`, Clipboard-Fallback für Electron/Browser/Terminal |
| Post-Processing | Claude Haiku 4.5, nur Satzzeichen + Whisper-Fehler |
| Landing Page | `web/` — Next.js + Tailwind, live auf Vercel |
| Git | Alles committed + gepusht |
| GitHub | **https://github.com/sahinelcoder/VoiceTool** |
| Vercel | **https://voicetool-app.vercel.app** |

## Was diese Session erledigt wurde

- **Streaming-Transkription implementiert** — lange Aufnahmen werden jetzt in Echtzeit verarbeitet:
  - `audio.py`: `drain_chunk()` gibt Audio zurück, behält 2s Overlap im Buffer
  - `transcribe.py`: `StreamingTranscriber` — Background-Worker mit Queue, sequentielle Chunk-Transkription
  - `main.py`: Timer alle 30s draint Chunks, `finalize()` am Ende fügt alles zusammen
  - Kurze Aufnahmen (<30s): wie bisher, alles am Ende
  - Lange Aufnahmen: ~1s Wartezeit statt Minuten
- **Dimension-Bug gefixt** — Overlap-Array nach drain war 1D, neue Callback-Chunks 2D → `.reshape(-1, 1)`

## Nächster Schritt — HIER WEITERMACHEN

**Desktop-App mit Settings-GUI bauen**

Ziel: Nativer macOS Settings-Dialog (kein Electron), erreichbar über Menu Bar → "Einstellungen".

Drei Tabs:

1. **Dictionary**
   - User-definierte Wörter die Whisper oft falsch erkennt (z.B. "Sahin", Fachbegriffe, Slang)
   - Liste mit Add/Remove, wird als YAML gespeichert
   - Wird an den Post-Processing-Prompt übergeben → Claude korrigiert diese Wörter gezielt

2. **Snippets**
   - Kürzel → Text-Expansion (z.B. "@@email" → "sahin@example.com")
   - Wird **nach** Post-Processing angewendet, vor Injection
   - Liste mit Kürzel + Expansion, Add/Remove

3. **General Settings**
   - Hotkey-Auswahl (Fn, F5, F6, Right Cmd, Arrow Combo)
   - Sprache (de, en, auto)
   - Post-Processing an/aus
   - Modell-Auswahl (Dropdown mit verfügbaren mlx-whisper Modellen)

**Technische Überlegungen:**
- GUI mit `pyobjc` (NSWindow, NSTabView) — passt zum bestehenden Stack, kein neues Framework
- Config bleibt `config.yaml` — GUI liest/schreibt dort
- Menu Bar bekommt "Einstellungen…" Item → öffnet Settings-Fenster
- Dictionary/Snippets als eigene YAML-Dateien oder in config.yaml eingebettet — zu Beginn mit User klären

## Entscheidungen

| Entscheidung | Gewählt | Grund |
|---|---|---|
| Whisper-Modell | **whisper-large-v3-turbo-german-f16-q4** | Benchmark-Sieger: korrekte Eigennamen, beste Satzzeichen, 0.99s, weniger RAM |
| Hotkey | Fn/Globe (🌐) | Ergonomisch, Quartz CGEventTap |
| Sprache | `de` (explizit) | Auto-Detection unzuverlässig bei kurzen Sätzen |
| Post-Processing | Claude Haiku 4.5 | Umgangssprache beibehalten, nur Satzzeichen |
| Text-Injection | `kAXSelectedTextAttribute` | Cursor-Insert, Clipboard-Fallback für Electron |
| App Bundle | PyInstaller | py2app hatte RecursionError mit mlx |
| Frontend | Next.js + Tailwind | Vercel-Deploy |
| Streaming | 30s Chunks + 2s Overlap | Balance zwischen Latenz und Transkriptionsqualität |
