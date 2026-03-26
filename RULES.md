# Rules

Coding-Standards für alle Dateien in diesem Projekt.

## Python

- Python 3.11+
- Type hints überall: `def record(duration: float) -> np.ndarray:`
- Docstrings für jede öffentliche Funktion (eine Zeile reicht)
- Keine globalen Variablen — Konfiguration wird als Parameter übergeben
- Exceptions immer mit Kontext: `raise RuntimeError("Audio device not found") from e`
- Kein `print()` im Produktionscode — nur `logging`

## Fehlerbehandlung

- Jede externe Operation (API, Mikrofon, Accessibility) muss try/except haben
- Bei Claude API Fehler → rohen Whisper-Text als Fallback verwenden, nie crashen
- Bei Injection-Fehler → immer Clipboard-Fallback versuchen, dann still loggen

## Sicherheit & Datenschutz

- Audio-Buffer nach Verarbeitung sofort aus dem RAM löschen
- API-Key niemals im Code oder in Logs — nur aus `config.yaml` lesen
- Kein Logging von Transkript-Inhalt (nur Metadaten wie Länge, App-Name)
- Keine Netzwerkanfragen außer Claude API (und nur wenn `post_processing: true`)

## Performance

- `mlx-whisper` immer im Streaming-Modus starten
- Audio-Recording in eigenem Thread — Hotkey-Listener darf nie blockieren
- Idle-Zustand: keine aktiven Threads außer dem Hotkey-Listener

## Dateistruktur

- Eine Aufgabe pro Datei — keine God-Module
- Imports am Anfang, keine Lazy Imports im Code
- `config.yaml` ist die einzige Quelle für alle Einstellungen

## macOS

- `pyobjc` Calls immer im Main Thread — sonst Crashes
- Accessibility API: Permission-Check beim Start, verständliche Fehlermeldung ausgeben
- Clipboard-Fallback: Original-Clipboard nach Injection wiederherstellen
