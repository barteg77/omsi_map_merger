# Copyright 2020, 2021, 2024 Bartosz Gajewski
#
# This file is part of OMSI Map Merger.
#
# OMSI Map Merger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# OMSI Map Merger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OMSI Map Merger. If not, see <http://www.gnu.org/licenses/>.

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import importlib

dragonmapper_root = os.path.dirname(importlib.import_module('dragonmapper').__file__)
charset_normalizer_root = os.path.dirname(importlib.import_module('charset_normalizer').__file__)

a = Analysis(['starter_loader.py'],
             pathex=['.'],
             binaries=[('gplv3-with-text-136x68.png', '.'),
                       ('texture/map/tile_0_0.map.0.dds', 'texture/map/')
                       ],
             datas=[('ailists_grammar.pg', '.'),
                    ('busstops_grammar.pg', '.'),
                    ('chrono_tile_grammar.pg', '.'),
                    ('global_config_grammar.pg', '.'),
                    ('station_links_grammar.pg', '.'),
                    ('tile_grammar.pg', '.'),
                    ('time_table_line_grammar.pg', '.'),
                    ('track_grammar.pg', '.'),
                    ('trip_grammar.pg', '.'),
                    ('LICENSE.txt', '.'),
                    ('LICENSE_charset_normalizer.txt', '.'),
                    ('LICENSE_Parglare.txt', '.'),
                    ('LICENSE_PySimpleGUI.txt', '.'),
                    ('LICENSE_Python.txt', '.'),
                    ('CREDITS.md', '.'),
                    (os.path.join(dragonmapper_root, 'data/transcriptions.csv'), 'dragonmapper/data/'),
                    (os.path.join(dragonmapper_root, 'data/hanzi_pinyin_words.tsv'), 'dragonmapper/data/'),
                    (os.path.join(dragonmapper_root, 'data/hanzi_pinyin_characters.tsv'), 'dragonmapper/data/'),
                    (os.path.join(charset_normalizer_root, 'assets/frequencies.json'), 'charset_normalizer/assets/')
                    ],
             hiddenimports=[],
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
          name='omsi_map_merger',
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
               name='omsi_map_merger')
