"""Tests für audio.py — AudioRecorder."""

import numpy as np
import pytest

from audio import AudioRecorder, SAMPLE_RATE, DTYPE


class TestAudioRecorder:
    def test_initial_state(self) -> None:
        recorder = AudioRecorder()
        assert not recorder.is_recording

    def test_stop_without_start_returns_empty(self) -> None:
        recorder = AudioRecorder()
        result = recorder.stop()
        assert isinstance(result, np.ndarray)
        assert result.size == 0

    def test_start_sets_recording_flag(self, mocker) -> None:
        mock_stream = mocker.MagicMock()
        mocker.patch("audio.sd.InputStream", return_value=mock_stream)

        recorder = AudioRecorder()
        recorder.start()

        assert recorder.is_recording
        mock_stream.start.assert_called_once()

    def test_start_twice_does_not_create_second_stream(self, mocker) -> None:
        mock_stream = mocker.MagicMock()
        mocker.patch("audio.sd.InputStream", return_value=mock_stream)

        recorder = AudioRecorder()
        recorder.start()
        recorder.start()  # zweiter Aufruf

        assert mock_stream.start.call_count == 1

    def test_stop_returns_concatenated_audio(self, mocker) -> None:
        mock_stream = mocker.MagicMock()
        mocker.patch("audio.sd.InputStream", return_value=mock_stream)

        recorder = AudioRecorder()
        recorder.start()

        # Simuliere Audio-Chunks
        chunk1 = np.ones((1024, 1), dtype=DTYPE) * 0.5
        chunk2 = np.ones((1024, 1), dtype=DTYPE) * 0.3
        recorder._chunks = [chunk1, chunk2]

        audio = recorder.stop()

        assert not recorder.is_recording
        assert audio.dtype == np.float32
        assert len(audio) == 2048
        mock_stream.stop.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_start_raises_on_device_error(self, mocker) -> None:
        import sounddevice as sd
        mocker.patch("audio.sd.InputStream", side_effect=sd.PortAudioError(-1))

        recorder = AudioRecorder()
        with pytest.raises(RuntimeError, match="Audio device"):
            recorder.start()

        assert not recorder.is_recording

    def test_audio_callback_appends_data(self, mocker) -> None:
        recorder = AudioRecorder()
        recorder._recording = True

        data = np.random.rand(1024, 1).astype(DTYPE)
        recorder._audio_callback(data, 1024, None, mocker.MagicMock(return_value=False, __bool__=lambda s: False))

        assert len(recorder._chunks) == 1
        np.testing.assert_array_equal(recorder._chunks[0], data)

    def test_custom_sample_rate(self, mocker) -> None:
        mock_input_stream = mocker.patch("audio.sd.InputStream", return_value=mocker.MagicMock())

        recorder = AudioRecorder(sample_rate=44100)
        recorder.start()

        call_kwargs = mock_input_stream.call_args[1]
        assert call_kwargs["samplerate"] == 44100
        assert recorder._sample_rate == 44100
