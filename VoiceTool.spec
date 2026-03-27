# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec für VoiceTool.app."""

import os
import site

block_cipher = None

# Site-packages Pfad für hidden imports
site_packages = site.getsitepackages()[0]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("config.yaml", "."),
    ],
    hiddenimports=[
        "audio",
        "transcribe",
        "context",
        "inject",
        "overlay",
        "postprocess",
        "pynput",
        "pynput.keyboard",
        "pynput.keyboard._darwin",
        "pynput._util",
        "pynput._util.darwin",
        "sounddevice",
        "numpy",
        "mlx",
        "mlx.core",
        "mlx_whisper",
        "whisper",
        "whisper.tokenizer",
        "anthropic",
        "yaml",
        "objc",
        "AppKit",
        "Foundation",
        "PyObjCTools",
        "PyObjCTools.AppHelper",
        "_sounddevice_data",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VoiceTool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # Kein Terminal-Fenster
    target_arch="arm64",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="VoiceTool",
)

app = BUNDLE(
    coll,
    name="VoiceTool.app",
    icon=None,  # TODO: App-Icon (.icns) hinzufügen
    bundle_identifier="com.sahinelcoder.voicetool",
    info_plist={
        "CFBundleName": "VoiceTool",
        "CFBundleDisplayName": "VoiceTool",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
        "LSMinimumSystemVersion": "13.0",
        "LSUIElement": True,  # Menu-Bar-App, kein Dock-Icon
        "NSMicrophoneUsageDescription": "VoiceTool benötigt Mikrofon-Zugriff für Sprach-Diktat.",
        "NSAppleEventsUsageDescription": "VoiceTool benötigt Accessibility-Zugriff für Text-Injection.",
    },
)
