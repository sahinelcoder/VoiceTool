"""Tests für inject.py — Text-Injection."""

from inject import inject_text, ELECTRON_APPS


class TestInjectText:
    def test_empty_text_returns_false(self) -> None:
        assert not inject_text("", "Safari")

    def test_electron_app_uses_clipboard(self, mocker) -> None:
        mock_paste = mocker.patch("inject._clipboard_paste", return_value=True)
        mocker.patch("inject._accessibility_inject")

        result = inject_text("hello", "Slack")

        assert result is True
        mock_paste.assert_called_once_with("hello")

    def test_non_electron_tries_accessibility_first(self, mocker) -> None:
        mock_ax = mocker.patch("inject._accessibility_inject", return_value=True)
        mock_paste = mocker.patch("inject._clipboard_paste")

        result = inject_text("hello", "Safari")

        assert result is True
        mock_ax.assert_called_once_with("hello")
        mock_paste.assert_not_called()

    def test_accessibility_failure_falls_back_to_clipboard(self, mocker) -> None:
        mocker.patch("inject._accessibility_inject", return_value=False)
        mock_paste = mocker.patch("inject._clipboard_paste", return_value=True)

        result = inject_text("hello", "Safari")

        assert result is True
        mock_paste.assert_called_once_with("hello")

    def test_no_fallback_returns_false(self, mocker) -> None:
        mocker.patch("inject._accessibility_inject", return_value=False)

        result = inject_text("hello", "Safari", use_clipboard_fallback=False)

        assert result is False

    def test_all_electron_apps_defined(self) -> None:
        expected = {"Slack", "Visual Studio Code", "Code", "Notion", "Discord", "Figma"}
        assert ELECTRON_APPS == expected
