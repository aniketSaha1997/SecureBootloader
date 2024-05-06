# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['flasher.py'],  # Main script
    pathex=[],
    binaries=[],
    datas=[
        ('cssStyles.py', '.'),  # Include the CSS file
        ('flasher_layout.py', '.'),  # Include the GUI layout script
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FlasherApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI app (no console)
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='FlasherApp',
)
