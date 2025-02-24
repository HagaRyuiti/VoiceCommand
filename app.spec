# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# 仮想環境のパスを追加
venv_path = os.path.abspath("./venv/Lib/site-packages")

a = Analysis(
    ['app.py'],
    pathex=[venv_path],  # 仮想環境のパスを追加
    binaries=[],
    datas=[("commands.db", ".")],  # データベースを含める
    hiddenimports=['speech_recognition', 'pyaudio', 'sqlite3'],  # 必要なモジュールを指定
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VoiceCommand',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    icon="statics/70d9bc364974adf1e0790e120753dc98_xxo.ico",
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
