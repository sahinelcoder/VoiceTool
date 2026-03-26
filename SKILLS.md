# Skills

## Code Review

Wenn du Code reviewst, prüfe in dieser Reihenfolge:

**1. Datenschutz**
- Wird Audio nach der Verarbeitung gelöscht?
- Werden Transkript-Inhalte geloggt?
- Verlässt Audio das Gerät (außer Claude API)?

**2. Fehlerbehandlung**
- Gibt es einen Fallback wenn die Claude API nicht antwortet?
- Gibt es einen Fallback wenn Accessibility-Injection fehlschlägt?
- Crasht die App wenn das Mikrofon nicht gefunden wird?

**3. Performance**
- Blockiert irgendwas den Hotkey-Listener?
- Laufen Audio-Recording und Transkription im richtigen Thread?
- Wird Speicher nach jeder Aufnahme freigegeben?

**4. macOS-Kompatibilität**
- Laufen pyobjc-Calls im Main Thread?
- Funktioniert Clipboard-Fallback für Electron-Apps?

**5. Security (vor jedem Commit)**
- Ist `ANTHROPIC_API_KEY` nirgends im Code hardcodiert?
- Wird API-Key nur aus `config.yaml` gelesen, nie geloggt?
- Wird Audio-Buffer nach Verarbeitung explizit gelöscht (`del buffer`)?
- Werden keine Transkript-Inhalte in Logfiles geschrieben?
- `/security-review` Skill durchlaufen lassen und Findings prüfen

---

## Security Audit

Skill: `getsentry/skills@security-review`

Wann ausführen:
- Vor jedem größeren Release
- Nach Änderungen an `postprocess.py`, `inject.py`, `config.yaml`
- Nach Hinzufügen neuer Dependencies

Was der Skill prüft:
- Hardcodierte Secrets und API-Keys
- Unsichere Dateioperationen
- Injection-Risiken
- Dependency-Schwachstellen

Befehl: `/security-review`

---

## Testing

Wenn du Tests schreibst oder ausführst:

**Unit Tests** (pytest)
- `audio.py` → Mock `sounddevice`, prüfe Buffer-Format (16kHz, Mono, float32)
- `transcribe.py` → Mock `mlx_whisper`, prüfe dass Rohtext zurückgegeben wird
- `context.py` → Mock `AppKit`, prüfe App-Name Extraktion
- `postprocess.py` → Mock Claude API, prüfe Fallback auf Rohtext bei Fehler
- `inject.py` → prüfe Clipboard-Fallback Logik ohne echte Injection

**Integration Tests**
- Vollständiger Durchlauf mit kurzer Audio-Datei (kein echtes Mikrofon nötig)
- Claude API mit echtem Key gegen Staging testen

**Manuelle App-Tests** (nach jeder größeren Änderung)
- Slack (Electron)
- Mail.app
- VS Code (Electron)
- Safari Adressleiste
- Notion (Electron)
- Terminal
