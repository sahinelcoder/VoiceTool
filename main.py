"""VoiceTool — Einstiegspunkt mit Hotkey-Listener."""

import logging
import signal
import sys
import threading
from pathlib import Path

import yaml

from pynput import keyboard

from audio import AudioRecorder
from context import get_active_app_name
from inject import inject_text
from postprocess import postprocess
from transcribe import Transcriber

logger = logging.getLogger(__name__)


def load_config(path: str = "config.yaml") -> dict:
    """Lädt die Konfiguration aus config.yaml."""
    config_path = Path(path)
    if not config_path.exists():
        logger.error("config.yaml nicht gefunden — kopiere config.example.yaml zu config.yaml")
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def setup_logging(debug: bool = False) -> None:
    """Konfiguriert das Logging."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def process_audio(
    recorder: AudioRecorder,
    transcriber: Transcriber,
    config: dict,
) -> None:
    """Verarbeitet aufgenommenes Audio: Transkription → Post-Processing → Injection."""
    import numpy as np

    audio = recorder.stop()

    if audio.size == 0:
        logger.warning("Leere Aufnahme, überspringe")
        return

    # App-Name im Main Thread auslesen (pyobjc-Anforderung)
    app_name = get_active_app_name()

    # Transkription
    try:
        raw_text = transcriber.transcribe(audio)
    except RuntimeError as e:
        logger.error("Transkription fehlgeschlagen: %s", e)
        return
    finally:
        # Audio-Buffer sofort löschen (Datenschutz)
        del audio

    if not raw_text.strip():
        logger.info("Kein Text erkannt")
        return

    logger.info("Rohtext: %d Zeichen", len(raw_text))

    # Post-Processing (optional)
    if config.get("post_processing", True):
        api_key = config.get("claude_api_key", "")
        if api_key and api_key != "sk-ant-...":
            text = postprocess(raw_text, app_name, api_key)
        else:
            logger.warning("Kein gültiger API-Key, überspringe Post-Processing")
            text = raw_text
    else:
        text = raw_text

    # Text injizieren
    use_fallback = config.get("clipboard_fallback", True)
    success = inject_text(text, app_name, use_clipboard_fallback=use_fallback)
    if not success:
        logger.error("Text-Injection fehlgeschlagen")


def main() -> None:
    """Startet VoiceTool."""
    config = load_config()
    setup_logging(config.get("debug", False))

    logger.info("VoiceTool startet...")

    # Transcriber vorladen
    transcriber = Transcriber(
        model=config.get("model", "mlx-community/whisper-small-mlx"),
        language=config.get("language"),
    )
    logger.info("Lade Whisper-Modell...")
    transcriber.load_model()

    recorder = AudioRecorder()

    # Hotkey-Listener
    hotkey_str = config.get("hotkey", "fn")
    logger.info("Hotkey: '%s' — drücken zum Aufnehmen, loslassen zum Stoppen", hotkey_str)

    def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Startet Recording bei Hotkey-Press."""
        if _key_matches(key, hotkey_str) and not recorder.is_recording:
            recorder.start()

    def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Stoppt Recording bei Hotkey-Release und verarbeitet Audio."""
        if _key_matches(key, hotkey_str) and recorder.is_recording:
            # Processing in separatem Thread um Listener nicht zu blockieren
            threading.Thread(
                target=process_audio,
                args=(recorder, transcriber, config),
                daemon=True,
            ).start()

    # Graceful Shutdown
    def signal_handler(sig: int, frame: object) -> None:
        logger.info("VoiceTool beendet")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        logger.info("VoiceTool bereit — warte auf Hotkey")
        listener.join()


def _key_matches(key: object, hotkey: str) -> bool:
    """Prüft ob der gedrückte Key dem konfigurierten Hotkey entspricht."""
    key_mapping: dict[str, list] = {
        "fn": [keyboard.Key.f5],  # fn direkt nicht abfangbar, F5 als Default
        "f5": [keyboard.Key.f5],
        "f6": [keyboard.Key.f6],
        "right_cmd": [keyboard.Key.cmd_r],
        "right_alt": [keyboard.Key.alt_r],
        "right_ctrl": [keyboard.Key.ctrl_r],
    }

    targets = key_mapping.get(hotkey.lower(), [])
    return key in targets


if __name__ == "__main__":
    main()
