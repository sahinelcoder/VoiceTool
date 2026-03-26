"""Claude API Post-Processing für Transkript-Bereinigung."""

import logging

import anthropic

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Du bist ein Text-Bereiniger für Voice-Dictation. "
    "Du erhältst einen rohen Transkript-Text und den Namen der App, in der der Text eingefügt wird. "
    "Bereinige den Text: korrigiere Grammatik, entferne Füllwörter, setze korrekte Satzzeichen. "
    "Behalte den Inhalt und Stil des Sprechers bei. "
    "Gib NUR den bereinigten Text zurück, ohne Erklärungen."
)


def postprocess(raw_text: str, app_name: str, api_key: str) -> str:
    """Bereinigt Rohtext mit Claude Haiku. Gibt bei Fehler den Rohtext zurück."""
    if not raw_text.strip():
        return raw_text

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"App: {app_name}\n\nRohtext: {raw_text}",
                }
            ],
        )
        cleaned = message.content[0].text.strip()
        logger.info("Post-Processing: %d → %d Zeichen", len(raw_text), len(cleaned))
        return cleaned

    except anthropic.APIError as e:
        logger.error("Claude API Fehler: %s", e)
        return raw_text
    except Exception as e:
        logger.error("Post-Processing fehlgeschlagen: %s", e)
        return raw_text
