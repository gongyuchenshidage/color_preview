# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['Color_Select.py', 'Color_Setting.py', 'gcode.py', 'gui_utils.py', 'locales.py', 'params.py', 'SelfDesign.py', 'Test.py', 'untitled.py', 'G:\\360MoveData\\Users\\Administrator\\Desktop\\test816'],
             binaries=[],
             datas=[],
             hiddenimports=['Color_Setting', 'untitled', 'Color_Select'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
