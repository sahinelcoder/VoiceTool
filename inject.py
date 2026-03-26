"""Text-Injection ins aktive Textfeld via Accessibility API + Clipboard-Fallback."""

import logging
import time

logger = logging.getLogger(__name__)

# Electron-Apps die keine Accessibility-Injection unterstützen
ELECTRON_APPS = {"Slack", "Visual Studio Code", "Code", "Notion", "Discord", "Figma"}


def inject_text(text: str, app_name: str, use_clipboard_fallback: bool = True) -> bool:
    """Injiziert Text ins aktive Textfeld. Gibt True bei Erfolg zurück."""
    if not text:
        return False

    # Electron-Apps direkt über Clipboard
    if use_clipboard_fallback and app_name in ELECTRON_APPS:
        logger.info("Electron-App '%s' erkannt, nutze Clipboard-Fallback", app_name)
        return _clipboard_paste(text)

    # Accessibility API versuchen
    if _accessibility_inject(text):
        return True

    # Fallback auf Clipboard
    if use_clipboard_fallback:
        logger.info("Accessibility fehlgeschlagen, Clipboard-Fallback")
        return _clipboard_paste(text)

    logger.error("Text-Injection fehlgeschlagen für '%s'", app_name)
    return False


def _accessibility_inject(text: str) -> bool:
    """Injiziert Text über die macOS Accessibility API."""
    try:
        from ApplicationServices import (
            AXUIElementCreateSystemWide,
            kAXFocusedUIElementAttribute,
            kAXValueAttribute,
        )

        system_wide = AXUIElementCreateSystemWide()
        err, focused = system_wide.copyAttributeValue_value_(kAXFocusedUIElementAttribute, None)

        if err != 0 or focused is None:
            logger.debug("Kein fokussiertes UI-Element gefunden (error: %d)", err)
            return False

        err = focused.setAttributeValue_value_(kAXValueAttribute, text)
        if err != 0:
            logger.debug("Konnte Wert nicht setzen (error: %d)", err)
            return False

        logger.info("Text via Accessibility API injiziert")
        return True

    except ImportError as e:
        logger.error("pyobjc ApplicationServices nicht verfügbar: %s", e)
        return False
    except Exception as e:
        logger.error("Accessibility-Injection fehlgeschlagen: %s", e)
        return False


def _clipboard_paste(text: str) -> bool:
    """Kopiert Text in die Zwischenablage und simuliert Cmd+V. Stellt Original wieder her."""
    try:
        from AppKit import NSPasteboard, NSPasteboardTypeString

        pasteboard = NSPasteboard.generalPasteboard()

        # Original-Clipboard sichern
        original = pasteboard.stringForType_(NSPasteboardTypeString)

        # Neuen Text setzen
        pasteboard.clearContents()
        pasteboard.setString_forType_(text, NSPasteboardTypeString)

        # Cmd+V simulieren
        _simulate_cmd_v()
        time.sleep(0.1)  # Kurz warten bis Paste verarbeitet ist

        # Original wiederherstellen
        if original is not None:
            pasteboard.clearContents()
            pasteboard.setString_forType_(original, NSPasteboardTypeString)

        logger.info("Text via Clipboard-Fallback eingefügt")
        return True

    except ImportError as e:
        logger.error("pyobjc AppKit nicht verfügbar: %s", e)
        return False
    except Exception as e:
        logger.error("Clipboard-Fallback fehlgeschlagen: %s", e)
        return False


def _simulate_cmd_v() -> None:
    """Simuliert Cmd+V Tastendruck."""
    from Quartz import (
        CGEventCreateKeyboardEvent,
        CGEventPost,
        CGEventSetFlags,
        kCGEventFlagMaskCommand,
        kCGHIDEventTap,
    )

    # 'v' keycode = 9
    event_down = CGEventCreateKeyboardEvent(None, 9, True)
    CGEventSetFlags(event_down, kCGEventFlagMaskCommand)
    event_up = CGEventCreateKeyboardEvent(None, 9, False)
    CGEventSetFlags(event_up, kCGEventFlagMaskCommand)

    CGEventPost(kCGHIDEventTap, event_down)
    CGEventPost(kCGHIDEventTap, event_up)
