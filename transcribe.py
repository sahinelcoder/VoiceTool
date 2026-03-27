"""mlx-whisper Integration für lokale Transkription."""

import logging
import queue
import threading
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


class StreamingTranscriber:
    """Transkribiert Audio-Chunks im Hintergrund während der Aufnahme läuft.

    Chunks werden über eine Queue empfangen und sequentiell transkribiert.
    Am Ende werden alle Teilergebnisse zusammengefügt.
    """

    def __init__(self, transcriber: Transcriber) -> None:
        self._transcriber = transcriber
        self._queue: queue.Queue[Optional[np.ndarray]] = queue.Queue()
        self._results: list[str] = []
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Startet den Background-Worker-Thread."""
        with self._lock:
            self._results = []
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        logger.info("StreamingTranscriber gestartet")

    def submit_chunk(self, audio: np.ndarray) -> None:
        """Übergibt einen Audio-Chunk zur Transkription."""
        if audio.size == 0:
            return
        self._queue.put(audio)
        logger.debug("Chunk submitted: %d Samples", audio.size)

    def finalize(self) -> str:
        """Signalisiert Ende, wartet auf alle Transkriptionen, gibt Gesamttext zurück."""
        self._queue.put(None)  # Sentinel
        if self._thread is not None:
            self._thread.join(timeout=30)
        with self._lock:
            text = " ".join(self._results)
        logger.info("Streaming-Transkription abgeschlossen: %d Teile, %d Zeichen",
                     len(self._results), len(text))
        return text.strip()

    def _worker(self) -> None:
        """Verarbeitet Chunks aus der Queue bis Sentinel (None) kommt."""
        chunk_idx = 0
        while True:
            audio = self._queue.get()
            if audio is None:
                break
            try:
                text = self._transcriber.transcribe(audio)
                if text.strip():
                    with self._lock:
                        self._results.append(text.strip())
                    logger.info("Chunk %d transkribiert: %d Zeichen", chunk_idx, len(text))
                chunk_idx += 1
            except RuntimeError as e:
                logger.error("Chunk %d fehlgeschlagen: %s", chunk_idx, e)
                chunk_idx += 1
            finally:
                del audio
