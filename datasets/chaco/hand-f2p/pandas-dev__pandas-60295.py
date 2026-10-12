import numpy as np

from pandas import DataFrame


def test_regex_replace_list_to_number_in_string_columns():
    df = DataFrame({"a": range(4), "b": list("ab.."), "c": ["a", "b", np.nan, "d"]})
    res = df.replace([r"\s*\.\s*", "b"], 0, regex=True)
    assert list(res["b"]) == ["a", 0, 0, 0]
    assert list(res["c"])[:2] == ["a", 0] and list(res["c"])[3] == "d"


def test_fillna_number_into_string_column():
    df = DataFrame({"A": [1.0, np.nan, 3.0], "foo": ["bar", np.nan, "bar"],
                    "B": [1.0, 2.0, 3.0]})
    result = df.fillna(value=0)
    assert result.loc[1, "A"] == 0
    assert result.loc[1, "foo"] == 0
    assert df.ffill().loc[1, "foo"] == "bar"
