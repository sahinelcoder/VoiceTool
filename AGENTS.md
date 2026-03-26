# Agents

Sub-Agents für fokussierte Aufgaben mit minimalem Kontextfenster.

---

## Audio Agent

**Aufgabe:** Alles rund um Mikrofon-Recording und mlx-whisper.

**Kontext laden:** `CLAUDE.md`, `RULES.md`, `audio.py`, `transcribe.py`

**Typische Aufgaben:**
- Audio-Recording implementieren oder debuggen
- mlx-whisper Modell wechseln oder optimieren
- Latenz der Transkription messen
- Audio-Buffer Format prüfen (16kHz, Mono, float32)

**Nicht zuständig für:** Text-Injection, Claude API, App-Kontext

---

## Inject Agent

**Aufgabe:** Text zuverlässig in das aktive Textfeld bringen.

**Kontext laden:** `CLAUDE.md`, `RULES.md`, `inject.py`, `context.py`

**Typische Aufgaben:**
- Accessibility API Integration implementieren
- Clipboard-Fallback für Electron-Apps (Slack, VS Code, Notion)
- App-Kompatibilität testen und Bugs fixen
- Original-Clipboard nach Injection wiederherstellen

**Nicht zuständig für:** Audio, Transkription, Claude API

---

## Testing Agent

**Aufgabe:** Tests schreiben und ausführen.

**Kontext laden:** `CLAUDE.md`, `RULES.md`, `SKILLS.md` (Testing-Abschnitt), die zu testende Datei

**Typische Aufgaben:**
- Unit Tests für eine einzelne Datei schreiben
- Fehlgeschlagene Tests debuggen
- Test-Coverage prüfen
- Manuelle App-Test-Checkliste durchgehen

**Nicht zuständig für:** Feature-Entwicklung

---

## Wie du einen Sub-Agent startest

Sag Claude Code explizit welchen Agenten du meinst:

```
"Starte den Audio Agent. Lade CLAUDE.md, RULES.md, audio.py und transcribe.py.
Aufgabe: [deine Aufgabe]"
```

Das hält das Kontextfenster klein und den Fokus scharf.
