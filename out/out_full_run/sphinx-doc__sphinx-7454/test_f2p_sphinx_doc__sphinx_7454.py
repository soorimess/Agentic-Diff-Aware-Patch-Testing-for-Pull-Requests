import zlib
from textwrap import dedent

import pytest

from sphinx.ext.intersphinx import normalize_intersphinx_mapping, load_mappings
from sphinx.testing.util import SphinxTestApp


def test_autodoc_typehints_links_for_None_and_int(sphinx_test_tempdir):
    """Regression test for handling of ``None`` in autodoc typehints (sphinx#7454).

    Ensure that when ``autodoc_typehints='signature'``, a return annotation of
    ``None`` is turned into a resolvable cross-reference (same as in
    ``description`` mode).  Before the fix, signatures showed a link for
    ``int`` but not for ``None``.
    """
    srcdir = sphinx_test_tempdir / 'sphinx_7454'
    if not srcdir.exists():
        srcdir.makedirs()

    # conf.py: add srcdir to sys.path so autodoc can import local module
    (srcdir / 'conf.py').write_text(dedent(
        """
        extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
        import os, sys
        sys.path.insert(0, os.path.abspath('.'))
        autodoc_typehints = 'signature'
        """
    ))

    # index.rst with automodule to document our tiny module
    (srcdir / 'index.rst').write_text(dedent(
        """
        .. automodule:: mymod
           :members:
        """
    ))

    # a small module with two functions: one returning None, one returning int
    (srcdir / 'mymod.py').write_text(dedent(
        """
        def f1() -> None:
            return None

        def f2() -> int:
            return 42
        """
    ))

    # create a minimal intersphinx inventory that maps 'None' as py:obj and
    # 'int' as py:class so missing-reference can resolve both
    inv_file = srcdir / 'inventory'
    header = (
        '# Sphinx inventory version 2\n'
        '# Project: test\n'
        '# Version: 1.0\n'
        '# The remainder of this file is compressed with zlib.\n'
    )
    body = (
        'None py:obj 1 library/constants.html#None -\n'
        'int py:class 1 library/functions.html#int -\n'
    )
    inv_file.write_bytes(header.encode('utf-8') + zlib.compress(body.encode('utf-8')))

    # build the docs
    app = SphinxTestApp(srcdir=srcdir)
    # point the intersphinx mapping to our inventory file
    app.config.intersphinx_mapping = {'https://docs.python.org/3': inv_file}
    app.config.intersphinx_cache_limit = 0

    # load the mappings (normally done on builder-inited)
    normalize_intersphinx_mapping(app, app.config)
    load_mappings(app)

    app.build()

    html = (app.outdir / 'index.html').read_text()

    # Both the 'None' and 'int' type hints should be resolved to external links
    assert 'library/functions.html#int' in html
    assert 'library/constants.html#None' in html

    app.cleanup()
