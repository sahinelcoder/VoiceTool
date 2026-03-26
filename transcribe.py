"""mlx-whisper Integration für lokale Transkription."""

import logging
import time
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


class Transcriber:
    """Transkribiert Audio-Buffer mit mlx-whisper."""

    def __init__(self, model: str = "mlx-community/whisper-small-mlx", language: Optional[str] = None) -> None:
        self._model = model
        self._language = language if language != "auto" else None
        self._loaded = False

    def load_model(self) -> None:
        """Lädt das Whisper-Modell vor (einmalig)."""
        if self._loaded:
            return
        try:
            import mlx_whisper  # noqa: F401
            logger.info("mlx-whisper Modell '%s' wird geladen...", self._model)
            # Warm-up: kurzes Dummy-Audio transkribieren um Modell in den RAM zu laden
            dummy = np.zeros(16000, dtype=np.float32)
            mlx_whisper.transcribe(dummy, path_or_hf_repo=self._model)
            self._loaded = True
            logger.info("Modell geladen")
        except Exception as e:
            raise RuntimeError(f"Whisper-Modell '{self._model}' konnte nicht geladen werden") from e

    def transcribe(self, audio: np.ndarray) -> str:
        """Transkribiert einen Audio-Buffer und gibt den Rohtext zurück."""
        if audio.size == 0:
            return ""

        import mlx_whisper

        if not self._loaded:
            self.load_model()

        start = time.perf_counter()
        try:
            options: dict = {"path_or_hf_repo": self._model}
            if self._language:
                options["language"] = self._language

            result = mlx_whisper.transcribe(audio, **options)
            text = result.get("text", "").strip()
            elapsed = time.perf_counter() - start
            logger.info("Transkription: %d Zeichen in %.2fs", len(text), elapsed)
            return text
        except Exception as e:
            logger.error("Transkription fehlgeschlagen: %s", e)
            raise RuntimeError("Transkription fehlgeschlagen") from e
