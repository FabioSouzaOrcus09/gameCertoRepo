block_cipher = None

a = Analysis(
    ['index.py'],
    pathex=['/home/orcus/Desktop/gameCertoRepo'],
    binaries=[],
    datas=[
         ('src/audio/*', 'src/audio'), 
        ('src/imagens/*', 'src/imagens'),
        ('src/font/*', 'src/font'),
        ('src/controlers/*', 'src/controlers')  # Incluindo controladores
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
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='meu_jogo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Altere para False se não quiser o console
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='meu_jogo',
)
