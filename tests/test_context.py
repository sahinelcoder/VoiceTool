"""Tests für context.py — App-Kontext."""

from context import get_active_app_name


class TestGetActiveAppName:
    def test_returns_app_name(self, mocker) -> None:
        mock_workspace = mocker.MagicMock()
        mock_workspace.activeApplication.return_value = {"NSApplicationName": "Safari"}

        mock_ns = mocker.MagicMock()
        mock_ns.sharedWorkspace.return_value = mock_workspace
        mocker.patch.dict("sys.modules", {"AppKit": mocker.MagicMock(NSWorkspace=mock_ns)})

        # Modul neu laden damit der Mock greift
        import importlib
        import context
        importlib.reload(context)

        result = context.get_active_app_name()
        assert result == "Safari"

    def test_returns_unknown_on_import_error(self, mocker) -> None:
        mocker.patch.dict("sys.modules", {"AppKit": None})

        import importlib
        import context
        importlib.reload(context)

        result = context.get_active_app_name()
        assert result == "Unknown"

    def test_returns_unknown_on_no_active_app(self, mocker) -> None:
        mock_workspace = mocker.MagicMock()
        mock_workspace.activeApplication.return_value = None

        mock_ns = mocker.MagicMock()
        mock_ns.sharedWorkspace.return_value = mock_workspace
        mocker.patch.dict("sys.modules", {"AppKit": mocker.MagicMock(NSWorkspace=mock_ns)})

        import importlib
        import context
        importlib.reload(context)

        result = context.get_active_app_name()
        assert result == "Unknown"
