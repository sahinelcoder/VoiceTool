"""py2app Build-Script für VoiceTool.app."""

from setuptools import setup

APP = ["main.py"]
DATA_FILES = [
    ("", ["config.yaml"]),
]

OPTIONS = {
    "argv_emulation": False,
    "iconfile": None,  # TODO: App-Icon (.icns) hinzufügen
    "plist": {
        "CFBundleName": "VoiceTool",
        "CFBundleDisplayName": "VoiceTool",
        "CFBundleIdentifier": "com.sahinelcoder.voicetool",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
        "LSMinimumSystemVersion": "13.0",
        "LSUIElement": True,  # Kein Dock-Icon — reine Menu-Bar-App
        "NSMicrophoneUsageDescription": "VoiceTool benötigt Mikrofon-Zugriff für Sprach-Diktat.",
        "NSAppleEventsUsageDescription": "VoiceTool benötigt Accessibility-Zugriff für Text-Injection.",
    },
    "packages": [
        "mlx",
        "mlx_whisper",
        "whisper",
        "sounddevice",
        "numpy",
        "pynput",
        "anthropic",
        "yaml",
        "objc",
        "AppKit",
        "Foundation",
    ],
    "includes": [
        "audio",
        "transcribe",
        "context",
        "inject",
        "overlay",
        "postprocess",
    ],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
