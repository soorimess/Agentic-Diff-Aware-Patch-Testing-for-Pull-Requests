import pandas as pd
from pandas.core.generic import NDFrame


def _concat_finalize_kwargs(monkeypatch, objs):
    seen = []
    original = NDFrame.__finalize__

    def spy(self, other, method=None, **kwargs):
        if method == "concat":
            seen.append(kwargs)
        return original(self, other, method=method, **kwargs)

    monkeypatch.setattr(NDFrame, "__finalize__", spy)
    pd.concat(objs)
    assert seen, "concat did not call __finalize__"
    return seen[-1]


def test_concat_hands_objs_to_finalize_for_frames(monkeypatch):
    a, b = pd.DataFrame({"x": [1]}), pd.DataFrame({"x": [2]})
    kwargs = _concat_finalize_kwargs(monkeypatch, [a, b])
    assert [o is a or o is b for o in kwargs["objs"]] == [True, True]


def test_concat_hands_objs_to_finalize_for_series(monkeypatch):
    a, b = pd.Series([1]), pd.Series([2])
    kwargs = _concat_finalize_kwargs(monkeypatch, [a, b])
    assert len(kwargs["objs"]) == 2


def test_concat_still_propagates_shared_attrs():
    a, b = pd.DataFrame({"x": [1]}), pd.DataFrame({"x": [2]})
    a.attrs = b.attrs = {"source": "s"}
    assert pd.concat([a, b]).attrs == {"source": "s"}
