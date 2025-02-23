# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['index.py'],  # Archivo principal de tu aplicación
    pathex=['C:\\Users\\joaqu\\OneDrive\\Escritorio\\proyecto\\Argo Inventory'],  # Ruta base de tu proyecto
    binaries=[],  # Archivos binarios adicionales
    datas=[
        ('src/templates', 'templates'),  # Incluye la carpeta src/templates como 'templates'
        ('src/static', 'static'),  # Incluye la carpeta src/static como 'static'
    ],
    hiddenimports=[],  # Módulos ocultos que PyInstaller no detecta automáticamente
    hookspath=[],  # Ruta a hooks personalizados
    hooksconfig={},  # Configuración de hooks
    runtime_hooks=[],  # Hooks de tiempo de ejecución
    excludes=['torch', 'torchvision', 'torchaudio'],  # Módulos a excluir
    noarchive=False,  # No comprimir en un archivo .pyz
    optimize=0,  # Sin optimización
)
pyz = PYZ(a.pure)  # Crear un archivo .pyz con los módulos de Python

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Argo Inventory',  # Nombre del ejecutable
    debug=False,  # Sin información de depuración
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir el ejecutable con UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Abrir una consola al ejecutar (cambia a False si es una GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'C:\Users\joaqu\OneDrive\Escritorio\proyecto\Argo Inventory\src\static\img\logo.ico'
)