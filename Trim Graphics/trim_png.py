"""
Trim whitespace in PNG files. Requires the convert utility (ImageMagick).
"""

import os
import sh

for fpath in os.listdir('.'):
    if fpath.endswith('.png'):
        print fpath
        sh.convert('-trim', fpath, fpath)
