"""Aktives Fenster auslesen via pyobjc."""

import logging

logger = logging.getLogger(__name__)


def get_active_app_name() -> str:
    """Gibt den Namen der aktiven App zurück (z.B. 'Safari', 'Slack')."""
    try:
        from AppKit import NSWorkspace

        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.activeApplication()
        if active_app:
            name = active_app.get("NSApplicationName", "Unknown")
            logger.info("Aktive App: %s", name)
            return name
    except ImportError as e:
        logger.error("pyobjc nicht verfügbar: %s", e)
    except Exception as e:
        logger.error("Fehler beim Auslesen der aktiven App: %s", e)

    return "Unknown"
