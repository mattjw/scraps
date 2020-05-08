"""
Path to the module that contains a function.
"""

import os.path
module_dir_path = os.path.split(os.path.abspath(__file__))[0]
print module_dir_path