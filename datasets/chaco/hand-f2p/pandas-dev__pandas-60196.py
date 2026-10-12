import inspect
import sys

import pandas as pd


def test_inspect_getmembers_without_jinja2(monkeypatch):
    # With jinja2 not installed, `.style` must raise AttributeError so that
    # inspect.getmembers (which only tolerates AttributeError) still works.
    monkeypatch.setitem(sys.modules, "jinja2", None)
    for name in ("pandas.io.formats.style", "pandas.io.formats.style_render"):
        monkeypatch.delitem(sys.modules, name, raising=False)
    df = pd.DataFrame({"a": [1, 2]})
    names = [n for n, _ in inspect.getmembers(df)]
    assert "style" not in names
    assert not hasattr(df, "style")
