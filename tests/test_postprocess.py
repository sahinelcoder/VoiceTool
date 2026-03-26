"""Tests für postprocess.py — Claude API Post-Processing."""

import pytest

from postprocess import postprocess


class TestPostprocess:
    def test_empty_text_returns_as_is(self) -> None:
        result = postprocess("", "Safari", "fake-key")
        assert result == ""

    def test_whitespace_only_returns_as_is(self) -> None:
        result = postprocess("   ", "Safari", "fake-key")
        assert result == "   "

    def test_successful_cleanup(self, mocker) -> None:
        mock_message = mocker.MagicMock()
        mock_message.content = [mocker.MagicMock(text="Bereinigter Text")]

        mock_client = mocker.MagicMock()
        mock_client.messages.create.return_value = mock_message
        mocker.patch("postprocess.anthropic.Anthropic", return_value=mock_client)

        result = postprocess("rohtext hier", "Safari", "sk-ant-test")

        assert result == "Bereinigter Text"
        mock_client.messages.create.assert_called_once()

    def test_api_error_returns_raw_text(self, mocker) -> None:
        import anthropic
        mock_client = mocker.MagicMock()
        mock_client.messages.create.side_effect = anthropic.APIError(
            message="rate limit",
            request=mocker.MagicMock(),
            body=None,
        )
        mocker.patch("postprocess.anthropic.Anthropic", return_value=mock_client)

        result = postprocess("mein rohtext", "Slack", "sk-ant-test")
        assert result == "mein rohtext"

    def test_generic_error_returns_raw_text(self, mocker) -> None:
        mock_client = mocker.MagicMock()
        mock_client.messages.create.side_effect = Exception("network")
        mocker.patch("postprocess.anthropic.Anthropic", return_value=mock_client)

        result = postprocess("fallback text", "Mail", "sk-ant-test")
        assert result == "fallback text"

    def test_passes_app_name_in_prompt(self, mocker) -> None:
        mock_message = mocker.MagicMock()
        mock_message.content = [mocker.MagicMock(text="clean")]

        mock_client = mocker.MagicMock()
        mock_client.messages.create.return_value = mock_message
        mocker.patch("postprocess.anthropic.Anthropic", return_value=mock_client)

        postprocess("test", "Notion", "sk-ant-test")

        call_args = mock_client.messages.create.call_args
        user_content = call_args[1]["messages"][0]["content"]
        assert "Notion" in user_content
