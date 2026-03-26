"""Mikrofon-Recording mit sounddevice."""

import logging
import threading
from typing import Optional

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"
BLOCKSIZE = 1024


class AudioRecorder:
    """Nimmt Audio vom Mikrofon auf, gesteuert durch start/stop."""

    def __init__(self, sample_rate: int = SAMPLE_RATE) -> None:
        self._sample_rate = sample_rate
        self._chunks: list[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None
        self._lock = threading.Lock()
        self._recording = False

    def start(self) -> None:
        """Startet die Aufnahme in einem eigenen Stream."""
        with self._lock:
            if self._recording:
                logger.warning("Recording läuft bereits")
                return
            self._chunks = []
            self._recording = True

        try:
            self._stream = sd.InputStream(
                samplerate=self._sample_rate,
                channels=CHANNELS,
                dtype=DTYPE,
                blocksize=BLOCKSIZE,
                callback=self._audio_callback,
            )
            self._stream.start()
            logger.info("Recording gestartet")
        except sd.PortAudioError as e:
            self._recording = False
            raise RuntimeError("Audio device not found or unavailable") from e

    def stop(self) -> np.ndarray:
        """Stoppt die Aufnahme und gibt den Audio-Buffer zurück."""
        with self._lock:
            if not self._recording:
                logger.warning("Kein aktives Recording")
                return np.array([], dtype=DTYPE)
            self._recording = False

        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except sd.PortAudioError as e:
                logger.error("Fehler beim Stoppen des Streams: %s", e)
            finally:
                self._stream = None

        if not self._chunks:
            return np.array([], dtype=DTYPE)

        audio = np.concatenate(self._chunks, axis=0).flatten()
        self._chunks = []
        logger.info("Recording gestoppt, %d Samples (%.1fs)", len(audio), len(audio) / self._sample_rate)
        return audio

    @property
    def is_recording(self) -> bool:
        """Gibt zurück ob gerade aufgenommen wird."""
        return self._recording

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        """Callback für den Audio-Stream — läuft in separatem Thread."""
        if status:
            logger.warning("Audio callback status: %s", status)
        if self._recording:
            self._chunks.append(indata.copy())
