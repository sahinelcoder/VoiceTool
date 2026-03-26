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
from overlay import RecordingOverlay
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
    overlay = RecordingOverlay()

    # Hotkey-Listener
    hotkey_str = config.get("hotkey", "arrow_combo")
    pressed_keys: set = set()

    if hotkey_str == "arrow_combo":
        logger.info("Hotkey: Pfeiltaste Links + Rechts gleichzeitig — halten zum Aufnehmen")
    else:
        logger.info("Hotkey: '%s' — drücken zum Aufnehmen, loslassen zum Stoppen", hotkey_str)

    def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Startet Recording bei Hotkey-Press."""
        if hotkey_str == "arrow_combo":
            if key in (keyboard.Key.left, keyboard.Key.right):
                pressed_keys.add(key)
                if (
                    keyboard.Key.left in pressed_keys
                    and keyboard.Key.right in pressed_keys
                    and not recorder.is_recording
                ):
                    logger.info("Combo erkannt — starte Aufnahme")
                    recorder.start()
                    overlay.show()
        elif _key_matches(key, hotkey_str) and not recorder.is_recording:
            recorder.start()
            overlay.show()

    def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Stoppt Recording bei Hotkey-Release und verarbeitet Audio."""
        if hotkey_str == "arrow_combo":
            if key in (keyboard.Key.left, keyboard.Key.right):
                pressed_keys.discard(key)
                if recorder.is_recording:
                    logger.info("Taste losgelassen — stoppe Aufnahme")
                    overlay.hide()
                    threading.Thread(
                        target=process_audio,
                        args=(recorder, transcriber, config),
                        daemon=True,
                    ).start()
        elif _key_matches(key, hotkey_str) and recorder.is_recording:
            overlay.hide()
            threading.Thread(
                target=process_audio,
                args=(recorder, transcriber, config),
                daemon=True,
            ).start()

    # Graceful Shutdown
    def signal_handler(sig: int, frame: object) -> None:
        logger.info("VoiceTool beendet")
        from PyObjCTools import AppHelper
        AppHelper.stopEventLoop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # pynput Listener im Background starten
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    logger.info("VoiceTool bereit — warte auf Hotkey")

    # AppKit Event Loop auf Main Thread (nötig für Overlay-Fenster)
    from AppKit import NSApplication
    from PyObjCTools import AppHelper

    NSApplication.sharedApplication()
    AppHelper.runEventLoop(installInterrupt=True)


def _key_matches(key: object, hotkey: str) -> bool:
    """Prüft ob der gedrückte Key dem konfigurierten Hotkey entspricht."""
    key_mapping: dict[str, list] = {
        "f5": [keyboard.Key.f5],
        "f6": [keyboard.Key.f6],
        "right_cmd": [keyboard.Key.cmd_r],
        "right_alt": [keyboard.Key.alt_r],
        "right_ctrl": [keyboard.Key.ctrl_r],
    }


if __name__ == "__main__":
    main()
