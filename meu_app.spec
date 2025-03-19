# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['setup.py'],  # Substitua pelo arquivo principal correto
    pathex=[],
    binaries=[],
    datas=[
        ("ativo.png", "."),
        ("ausente.png", "."),
        ("comestoque.png", "."),
        ("database", "database"),
        ("delete.png", "."),
        ("esgotado.png", "."),
        ("functions", "functions"),
        ("generate.py", "."),
        ("GIFLOAD.gif", "."),
        ("renovar.png", "."),
        ("view", "view"),
        ("zeromq.py", "."),
    ],
    hiddenimports=['file_principal_rc'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['__pycache__'],
    noarchive=False,
    optimize=1,  # Otimização básica
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='meu_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Ocultar console ao executar
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)