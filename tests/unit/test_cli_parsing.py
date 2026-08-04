import pytest

from texthooks.fix_ligatures import LIGATURE_FIXER
from texthooks.fix_smartquotes import (
    DEFAULT_DOUBLE_QUOTE_CODEPOINTS,
    DEFAULT_SINGLE_QUOTE_CODEPOINTS,
)
from texthooks.fix_smartquotes import QuoteFixer as _QuoteFixer


def QuoteFixer():
    return _QuoteFixer("fake docstring", {})


def test_fix_ligatures_arg_parsing():
    args1 = LIGATURE_FIXER._parse_args(argv=["foo", "bar"])
    assert list(args1.files) == ["foo", "bar"]
    assert args1.show_changes is False

    args2 = LIGATURE_FIXER._parse_args(argv=["foo", "--show-changes"])
    assert list(args2.files) == ["foo"]
    assert args2.show_changes is True


def test_fix_smartquotes_arg_parsing():
    args1 = QuoteFixer()._parse_args(argv=["foo", "bar"])
    assert list(args1.files) == ["foo", "bar"]
    assert args1.show_changes is False
    assert args1.double_quote_codepoints == DEFAULT_DOUBLE_QUOTE_CODEPOINTS
    assert args1.single_quote_codepoints == DEFAULT_SINGLE_QUOTE_CODEPOINTS

    args2 = QuoteFixer()._parse_args(argv=["foo", "--show-changes"])
    assert list(args2.files) == ["foo"]
    assert args2.show_changes is True
    assert args2.double_quote_codepoints == DEFAULT_DOUBLE_QUOTE_CODEPOINTS
    assert args2.single_quote_codepoints == DEFAULT_SINGLE_QUOTE_CODEPOINTS

    args3 = QuoteFixer()._parse_args(
        argv=["foo", "--double-quote-codepoints", "FF02,201C"]
    )
    assert list(args3.files) == ["foo"]
    assert args3.show_changes is False
    assert list(args3.double_quote_codepoints) == ["FF02", "201C"]
    assert args3.single_quote_codepoints == DEFAULT_SINGLE_QUOTE_CODEPOINTS

    args4 = QuoteFixer()._parse_args(
        argv=["foo", "--single-quote-codepoints", "FF07,201B"]
    )
    assert list(args4.files) == ["foo"]
    assert args4.show_changes is False
    assert args2.double_quote_codepoints == DEFAULT_DOUBLE_QUOTE_CODEPOINTS
    assert list(args4.single_quote_codepoints) == ["FF07", "201B"]


@pytest.mark.parametrize("fixer", [LIGATURE_FIXER, QuoteFixer()])
def test_invalid_color_opt(fixer):
    with pytest.raises(SystemExit) as excinfo:
        fixer._parse_args(argv=["foo", "--color", "bar"])
    err = excinfo.value
    assert err.code == 2
