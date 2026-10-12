from pandas.core.indexes.base import trim_front


def test_trim_front_strips_common_leading_tabs():
    # Leading whitespace shared by every string is trimmed, not only spaces.
    assert trim_front(["\ta", "\tbb"]) == ["a", "bb"]


def test_trim_front_strips_smallest_common_indent():
    assert trim_front(["\t\ta", "\tb"]) == ["\ta", "b"]
