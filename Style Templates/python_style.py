# -*- coding: utf-8 -*-
#
# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     20??
# License:  MIT License
#           http://opensource.org/licenses/MIT

"""
?? Module/script description. ??

Preferred style:
    Sphinx Napoleon Google-like auto-doc format:
    http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html

Other resources:
    * Sphinx reStructuredText primer:
        http://sphinx-doc.org/rest.html
    Google-style ReST docstrings Template:
        http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html
    Sphinx Napoleon -- AutoDoc-able Google-like docstrings:
        http://sphinxcontrib-napoleon.readthedocs.org/en/latest/
    LaunchPad Python Style Guide:
        https://dev.launchpad.net/PythonStyleGuide
    Google Python Style Guide:
        http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
    PEP 8:
        https://www.python.org/dev/peps/pep-0008/
    NumPy Style Doc docstrings (via sphinx-napoleon):
        http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_numpy.html

---
"""

__author__ = "Matt J Williams"
__author_email__ = "mattjw@mattjw.net"
__license__ = "MIT"
__copyright__ = "Copyright (c) 20?? Matt J Williams"

import standard_libs
import more_standard_libs

import third_party_libs
import more_third_party_libs

import package_modules
import more_package_modules


def example_generator(n):
    """
    Generators have a ``Yields`` section instead of a ``Returns`` section.

    Args:
      n (int): The upper limit of the range to generate, from 0 to `n` - 1

    Yields:
      int: The next number in the range of 0 to `n` - 1

    Examples:
      Examples should be written in doctest format, and should illustrate how
      to use the function.

      >>> print [i for i in example_generator(4)]
      [0, 1, 2, 3]
    """
    for i in range(n):
        yield i


def module_level_function(param1, param2=None, *args, **kwargs):
    """
    This is an example of a module level function.

    Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    If the parameter itself is optional, it should be noted by adding
    ", optional" to the type. If \*args or \*\*kwargs are accepted, they
    should be listed as \*args and \*\*kwargs.

    The format for a parameter is::

        name (type): description
          The description may span multiple lines. Following
          lines should be indented.

          Multiple paragraphs are supported in parameter
          descriptions.

    Args:
      param1 (int): The first parameter.
      param2 (str, optional): The second parameter. Defaults to None.
        Second line of description should be indented.
      *args: Variable length argument list.
      **kwargs: Arbitrary keyword arguments.

    Returns:
      bool: True if successful, False otherwise.

      The return type is optional and may be specified at the beginning of
      the ``Returns`` section followed by a colon.

      The ``Returns`` section may span multiple lines and paragraphs.
      Following lines should be indented to match the first line.

      The ``Returns`` section supports any reStructuredText formatting,
      including literal blocks::

          {
              'param1': param1,
              'param2': param2
          }

    Raises:
      AttributeError: The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
      ValueError: If `param2` is equal to `param1`.
    """
    if param1 == param2:
        raise ValueError('param1 may not be equal to param2')
    return True

def main():
    pass

if __name__ == "__main__":
    main()
