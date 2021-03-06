#!/usr/bin/env python
###############################################################################
# $Id$
#
#  Project:  PROJ
#  Purpose:  Populate grid_alternatives with NAD83 -> NAD83(HPGN/HARN) grids
#  Author:   Even Rouault <even.rouault at spatialys.com>
#
###############################################################################
#  Copyright (c) 2018, Even Rouault <even.rouault at spatialys.com>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
###############################################################################

import os

nadcon_grids = ['conus', 'alaska', 'hawaii',
                'prvi', 'stgeorge', 'stlrnc', 'stpaul']

hpgn_grids = [
    'alhpgn.gsb',
    'arhpgn.gsb',
    'azhpgn.gsb',
    #'c1hpgn.gsb',  -- Not used in EPSG
    #'c2hpgn.gsb',  -- Not used in EPSG
    'cnhpgn.gsb',
    'cohpgn.gsb',
    'cshpgn.gsb',
    'emhpgn.gsb',
    'eshpgn.gsb',
    'ethpgn.gsb',
    ('flhpgn.gsb', 'FL'),
    'gahpgn.gsb',
    'guhpgn.gsb',
    'hihpgn.gsb',
    'iahpgn.gsb',
    'ilhpgn.gsb',
    'inhpgn.gsb',
    'kshpgn.gsb',
    'kyhpgn.gsb',
    'lahpgn.gsb',
    ('mdhpgn.gsb', 'MD'),
    'mehpgn.gsb',
    'mihpgn.gsb',
    'mnhpgn.gsb',
    'mohpgn.gsb',
    'mshpgn.gsb',
    'nbhpgn.gsb',
    'nchpgn.gsb',
    'ndhpgn.gsb',
    'nehpgn.gsb',
    'njhpgn.gsb',
    'nmhpgn.gsb',
    'nvhpgn.gsb',
    'nyhpgn.gsb',
    'ohhpgn.gsb',
    'okhpgn.gsb',
    'pahpgn.gsb',
    'pvhpgn.gsb',
    'schpgn.gsb',
    'sdhpgn.gsb',
    ('tnhpgn.gsb', 'TN'),
    'uthpgn.gsb',
    'vahpgn.gsb',
    ('wihpgn.gsb', 'WI'),
    'wmhpgn.gsb',
    ('wohpgn.gsb', 'WO'),
    'wshpgn.gsb',
    'wthpgn.gsb',
    'wvhpgn.gsb',
    'wyhpgn.gsb',
]

script_dir_name = os.path.dirname(os.path.realpath(__file__))
sql_dir_name = os.path.join(os.path.dirname(script_dir_name), 'data', 'sql')

f = open(os.path.join(sql_dir_name, 'grid_alternatives_generated') + '.sql', 'wb')
f.write("--- This file has been generated by scripts/build_grid_alternatives_generated.py. DO NOT EDIT !\n\n".encode('UTF-8'))

f.write("-- NADCON (NAD27 -> NAD83) entries\n\n".encode('UTF-8'))

for grid in nadcon_grids:
    sql = """INSERT INTO grid_alternatives(original_grid_name,
                              proj_grid_name,
                              proj_grid_format,
                              proj_method,
                              inverse_direction,
                              package_name,
                              url, direct_download, open_license, directory)
                      VALUES ('%s',
                              '%s',
                              'CTable2',
                              'hgridshift',
                              0,
                              'proj-datumgrid',
                              NULL, NULL, NULL, NULL);""" % (grid + '.las', grid)
    f.write((sql + '\n').encode('UTF-8'))


f.write("-- NAD83 -> NAD83(HPGN) entries\n\n".encode('UTF-8'))

for row in hpgn_grids:
    try:
        ntv2_name, ctable2_name = row
    except:
        ntv2_name = row
        ctable2_name = None
    las_filename = ntv2_name[0:-4] + ".las"
    if ctable2_name:
        sql = """INSERT INTO grid_alternatives(original_grid_name,
                              proj_grid_name,
                              proj_grid_format,
                              proj_method,
                              inverse_direction,
                              package_name,
                              url, direct_download, open_license, directory)
                      VALUES ('%s',
                              '%s',
                              'CTable2',
                              'hgridshift',
                              0,
                              'proj-datumgrid',
                              NULL, NULL, NULL, NULL);""" % (las_filename, ctable2_name)
    else:
        sql = """INSERT INTO grid_alternatives(original_grid_name,
                              proj_grid_name,
                              proj_grid_format,
                              proj_method,
                              inverse_direction,
                              package_name,
                              url, direct_download, open_license, directory)
                      VALUES ('%s',
                              '%s',
                              'NTv2',
                              'hgridshift',
                              0,
                              'proj-datumgrid-north-america',
                              NULL, NULL, NULL, NULL);""" % (las_filename, ntv2_name)
    f.write((sql + '\n').encode('UTF-8'))

f.close()
