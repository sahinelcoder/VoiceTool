"""VoiceTool — Einstiegspunkt mit Hotkey-Listener."""

import logging
import signal
import sys
import threading
from pathlib import Path

import yaml

from pynput import keyboard

from AppKit import (
    NSApplication,
    NSMenu,
    NSMenuItem,
    NSStatusBar,
    NSVariableStatusItemLength,
)
from PyObjCTools import AppHelper
from Quartz import (
    CGEventGetFlags,
    CGEventGetType,
    CGEventTapCreate,
    CFMachPortCreateRunLoopSource,
    CFRunLoopAddSource,
    CFRunLoopGetCurrent,
    CGEventMaskBit,
    CGEventTapEnable,
    kCGEventFlagMaskSecondaryFn,
    kCGEventTapOptionDefault,
    kCGHeadInsertEventTap,
    kCGSessionEventTap,
    kCGEventFlagsChanged,
    kCFRunLoopCommonModes,
)

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


def start_fn_key_listener(on_fn_down: callable, on_fn_up: callable) -> None:
    """Startet einen Quartz Event Tap für die Fn/Globe-Taste (🌐).

    pynput kann die Fn-Taste nicht erkennen — macOS fängt sie auf Hardware-Ebene ab.
    Wir nutzen CGEventTap um flagsChanged-Events mit dem Fn-Flag zu monitoren.
    """
    fn_pressed = False

    def callback(proxy, event_type, event, refcon):
        nonlocal fn_pressed
        flags = CGEventGetFlags(event)
        fn_is_down = bool(flags & kCGEventFlagMaskSecondaryFn)

        if fn_is_down and not fn_pressed:
            fn_pressed = True
            on_fn_down()
        elif not fn_is_down and fn_pressed:
            fn_pressed = False
            on_fn_up()

        return event

    tap = CGEventTapCreate(
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        CGEventMaskBit(kCGEventFlagsChanged),
        callback,
        None,
    )

    if tap is None:
        logger.error("CGEventTap konnte nicht erstellt werden — Accessibility-Berechtigung fehlt?")
        return

    source = CFMachPortCreateRunLoopSource(None, tap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(), source, kCFRunLoopCommonModes)
    CGEventTapEnable(tap, True)
    logger.info("Fn-Key-Listener aktiv (Quartz Event Tap)")


class StatusBarController:
    """Menu-Bar-Icon oben rechts (bei Uhr/Akku)."""

    ICON_IDLE = "🎙"
    ICON_RECORDING = "🔴"

    def __init__(self):
        self._status_item = None
        self._menu = None

    def setup(self) -> None:
        """Erstellt das Status-Bar-Item mit Dropdown-Menü."""
        status_bar = NSStatusBar.systemStatusBar()
        self._status_item = status_bar.statusItemWithLength_(
            NSVariableStatusItemLength
        )
        button = self._status_item.button()
        button.setTitle_(self.ICON_IDLE)

        # Dropdown-Menü
        self._menu = NSMenu.alloc().init()

        status_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "VoiceTool — Bereit", None, ""
        )
        status_item.setEnabled_(False)
        self._menu.addItem_(status_item)

        self._menu.addItem_(NSMenuItem.separatorItem())

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Beenden", "terminate:", "q"
        )
        self._menu.addItem_(quit_item)

        self._status_item.setMenu_(self._menu)
        logger.info("Menu-Bar-Icon aktiv")

    def set_recording(self, recording: bool) -> None:
        """Wechselt Icon und Status-Text je nach Aufnahme-Status."""
        def _update():
            if self._status_item is None:
                return
            button = self._status_item.button()
            status_text = self._menu.itemAtIndex_(0)
            if recording:
                button.setTitle_(self.ICON_RECORDING)
                status_text.setTitle_("VoiceTool — Aufnahme...")
            else:
                button.setTitle_(self.ICON_IDLE)
                status_text.setTitle_("VoiceTool — Bereit")

        if threading.current_thread() is threading.main_thread():
            _update()
        else:
            AppHelper.callAfter(_update)


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
    status_bar = StatusBarController()

    # Hotkey-Listener
    hotkey_str = config.get("hotkey", "fn")
    pressed_keys: set = set()

    def _start_recording():
        if not recorder.is_recording:
            logger.info("Starte Aufnahme")
            recorder.start()
            overlay.show()
            status_bar.set_recording(True)

    def _stop_recording():
        if recorder.is_recording:
            logger.info("Stoppe Aufnahme")
            overlay.hide()
            status_bar.set_recording(False)
            threading.Thread(
                target=process_audio,
                args=(recorder, transcriber, config),
                daemon=True,
            ).start()

    if hotkey_str == "fn":
        logger.info("Hotkey: Fn/Globe (🌐) — halten zum Aufnehmen")
    elif hotkey_str == "arrow_combo":
        logger.info("Hotkey: Pfeiltaste Links + Rechts gleichzeitig — halten zum Aufnehmen")
    else:
        logger.info("Hotkey: '%s' — drücken zum Aufnehmen, loslassen zum Stoppen", hotkey_str)

    def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Startet Recording bei Hotkey-Press (pynput)."""
        if hotkey_str == "arrow_combo":
            if key in (keyboard.Key.left, keyboard.Key.right):
                pressed_keys.add(key)
                if keyboard.Key.left in pressed_keys and keyboard.Key.right in pressed_keys:
                    _start_recording()
        elif hotkey_str != "fn" and _key_matches(key, hotkey_str):
            _start_recording()

    def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
        """Stoppt Recording bei Hotkey-Release (pynput)."""
        if hotkey_str == "arrow_combo":
            if key in (keyboard.Key.left, keyboard.Key.right):
                pressed_keys.discard(key)
                _stop_recording()
        elif hotkey_str != "fn" and _key_matches(key, hotkey_str):
            _stop_recording()

    # Graceful Shutdown
    def signal_handler(sig: int, frame: object) -> None:
        logger.info("VoiceTool beendet")
        AppHelper.stopEventLoop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # pynput Listener für arrow_combo und andere Keys
    if hotkey_str != "fn":
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

    logger.info("VoiceTool bereit — warte auf Hotkey")

    # AppKit Event Loop auf Main Thread
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(1)  # NSApplicationActivationPolicyAccessory — kein Dock-Icon
    status_bar.setup()

    # Fn-Key-Listener auf dem Main Thread (braucht CFRunLoop)
    if hotkey_str == "fn":
        start_fn_key_listener(on_fn_down=_start_recording, on_fn_up=_stop_recording)

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
