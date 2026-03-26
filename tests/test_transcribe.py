"""Tests für transcribe.py — Transcriber."""

import numpy as np
import pytest

from transcribe import Transcriber


class TestTranscriber:
    def test_empty_audio_returns_empty_string(self) -> None:
        transcriber = Transcriber()
        result = transcriber.transcribe(np.array([], dtype=np.float32))
        assert result == ""

    def test_transcribe_returns_text(self, mocker) -> None:
        mock_mlx = mocker.MagicMock()
        mock_mlx.transcribe.return_value = {"text": " Hallo Welt "}
        mocker.patch.dict("sys.modules", {"mlx_whisper": mock_mlx})

        transcriber = Transcriber(model="test-model")
        transcriber._loaded = True

        audio = np.random.rand(16000).astype(np.float32)
        result = transcriber.transcribe(audio)

        assert result == "Hallo Welt"
        mock_mlx.transcribe.assert_called_once()

    def test_transcribe_passes_language(self, mocker) -> None:
        mock_mlx = mocker.MagicMock()
        mock_mlx.transcribe.return_value = {"text": "test"}
        mocker.patch.dict("sys.modules", {"mlx_whisper": mock_mlx})

        transcriber = Transcriber(model="test-model", language="de")
        transcriber._loaded = True

        audio = np.random.rand(16000).astype(np.float32)
        transcriber.transcribe(audio)

        call_kwargs = mock_mlx.transcribe.call_args[1]
        assert call_kwargs["language"] == "de"

    def test_auto_language_sets_none(self) -> None:
        transcriber = Transcriber(language="auto")
        assert transcriber._language is None

    def test_transcribe_error_raises_runtime_error(self, mocker) -> None:
        mock_mlx = mocker.MagicMock()
        mock_mlx.transcribe.side_effect = Exception("model error")
        mocker.patch.dict("sys.modules", {"mlx_whisper": mock_mlx})

        transcriber = Transcriber()
        transcriber._loaded = True

        audio = np.random.rand(16000).astype(np.float32)
        with pytest.raises(RuntimeError, match="Transkription fehlgeschlagen"):
            transcriber.transcribe(audio)

    def test_load_model_failure_raises(self, mocker) -> None:
        mock_mlx = mocker.MagicMock()
        mock_mlx.transcribe.side_effect = Exception("load failed")
        mocker.patch.dict("sys.modules", {"mlx_whisper": mock_mlx})

        transcriber = Transcriber(model="nonexistent")
        with pytest.raises(RuntimeError, match="konnte nicht geladen werden"):
            transcriber.load_model()
