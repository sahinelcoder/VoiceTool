# Setup

Einmalige Einrichtung des Projekts – Skills, Dependencies, Permissions.

---

## 1. Claude Code Skills installieren

### Pflicht – sofort installieren

```bash
# Code-Qualität: First-Draft → Second-Draft automatisch
npx skills add anthropics/claude-code --skill simplify

# Security Review: Sentry-Team, 17 Vulnerability-Guides, wenig False Positives
npx skills install getsentry/skills@security-review
```

### Phase 2 – wenn Landing Page gebaut wird

```bash
# Frontend UI die nicht generisch "AI-made" aussieht
npx skills add anthropics/claude-code --skill frontend-design

# End-to-End Tests für Landing Page
npx skills install alirezarezvani/claude-skills playwright-pro
```

### Nur aus vertrauenswürdigen Quellen installieren
Skills haben vollen Zugriff auf Filesystem und Shell.
Nur Anthropic-official und verifizierte Publisher (Sentry, Trail of Bits).

---

## 2. Python Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
mlx-whisper
sounddevice
numpy
pynput
pyobjc-framework-Cocoa
pyobjc-framework-ApplicationServices
anthropic
pyyaml
pytest
pytest-mock
```

---

## 3. Whisper-Modell herunterladen

```bash
python -c "import mlx_whisper; mlx_whisper.load_models.load_model('mlx-community/whisper-large-v3-mlx')"
```

Größe: ~3 GB. Einmalig, läuft dann vollständig lokal.

---

## 4. config.yaml anlegen

```bash
cp config.example.yaml config.yaml
```

Dann `config.yaml` bearbeiten:

```yaml
hotkey: "fn"
model: "mlx-community/whisper-large-v3-mlx"
language: "auto"
claude_api_key: "sk-ant-..."   # niemals committen
post_processing: true
clipboard_fallback: true
startup_sound: false
debug: false
```

**Wichtig:** `config.yaml` ist in `.gitignore` – API-Key niemals in Git.

---

## 5. macOS Permissions setzen

Unter **Systemeinstellungen → Datenschutz & Sicherheit:**

| Permission | Warum | Ohne geht nicht |
|---|---|---|
| Mikrofon | Audio aufnehmen | Recording |
| Bedienungshilfen | Text injizieren | Inject.py |

Permissions für Terminal oder deine Python-Umgebung aktivieren.

---

## 6. Projekt-Struktur verifizieren

```
voicetool/
├── CLAUDE.md       ✓ Hauptkontext für Claude Code
├── RULES.md        ✓ Coding Standards
├── SKILLS.md       ✓ Review & Testing
├── AGENTS.md       ✓ Sub-Agent Definitionen
├── SETUP.md        ✓ Diese Datei
├── config.yaml     ✓ (nicht in Git)
├── .gitignore      → config.yaml, __pycache__, .env
└── requirements.txt ✓
```

---

## 7. Erster Start

```bash
# Security Check vor erstem Commit
/security-review

# Tests laufen lassen
pytest tests/

# App starten
python main.py
```
