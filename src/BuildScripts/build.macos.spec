# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wnp.py'],
    pathex=['.', 'lib', 'ui'],
    binaries=[],
    datas=[],
    hiddenimports=[ 
        'lib.CheckApplicable',
        'lib.config',
        'lib.environment',
        'lib.loggers',
        'lib.NoaaObservationRun',
        'lib.run_commands_linux',
        'lib.run_commands',
        'lib.singleton',
        'lib.windows_utilities',
    ], 
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
    [],
    exclude_binaries=True,
    name='wnp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wnp',
)
