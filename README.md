# VoiceTool

Voice-Dictation for macOS. Hold hotkey, speak, release — cleaned text appears in the active text field.

**[Live Demo](https://voicetool-app.vercel.app)** | **[GitHub](https://github.com/sahinelcoder/VoiceTool)**

## Features

- **100% Local** — Audio never leaves your device. Whisper runs on Apple Neural Engine via `mlx-whisper`
- **Fast** — Under 1.5 seconds end-to-end on M3
- **Works everywhere** — Safari, Slack, VS Code, Notion, Mail, and any other app
- **Live waveform** — Visual feedback with audio-reactive bars while recording
- **Smart cleanup** — Optional post-processing via Claude API (keeps your exact wording, just adds punctuation)
- **Privacy first** — Audio is deleted immediately after transcription. No logs, no cloud upload

## How it works

```
Hold hotkey → Record audio → Release hotkey
→ mlx-whisper transcribes locally
→ App name detected (pyobjc)
→ Claude Haiku cleans up punctuation (optional)
→ Text injected into active text field
```

## Requirements

- macOS Ventura or later
- Apple Silicon (M1, M2, M3, M4)
- Python 3.12+
- ~800 MB RAM for Whisper model
- Microphone permission
- Accessibility permission (for text injection)

## Installation

```bash
# Clone
git clone https://github.com/sahinelcoder/VoiceTool.git
cd VoiceTool

# Virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Config
cp config.example.yaml config.yaml
# Edit config.yaml — add your Claude API key if you want post-processing
```

## Usage

```bash
source .venv/bin/activate
python main.py
```

**Hotkey:** Press both arrow keys (left + right) simultaneously and hold while speaking. Release to stop recording.

The waveform overlay appears above the Dock while recording. Text is inserted into whatever app is focused.

## Configuration

Edit `config.yaml`:

```yaml
hotkey: "arrow_combo"           # Both arrow keys simultaneously
model: "mlx-community/whisper-large-v3-mlx-4bit"
language: "de"                  # or "en", "fr", etc.
claude_api_key: "sk-ant-..."   # Optional, for punctuation cleanup
post_processing: true           # Set false to skip Claude API
clipboard_fallback: true        # Clipboard paste for Electron apps
```

## Tech Stack

| Layer | Tool |
|---|---|
| Transcription | `mlx-whisper` (Neural Engine) |
| Audio | `sounddevice` + `numpy` |
| Hotkey | `pynput` |
| App context | `pyobjc` + `AppKit` |
| Post-processing | Claude API (Haiku) |
| Text injection | Accessibility API + clipboard fallback |
| Overlay | `AppKit` NSWindow + NSTimer |

## License

MIT
