import pytest

from texthooks.fix_ligatures import LIGATURE_FIXER
from texthooks.fix_smartquotes import (
    DEFAULT_DOUBLE_QUOTE_CODEPOINTS,
    DEFAULT_SINGLE_QUOTE_CODEPOINTS,
)
from texthooks.fix_smartquotes import QuoteFixer as _QuoteFixer


def QuoteFixer():
    return _QuoteFixer("fake docstring", {})


def _extra_quote_codepoints(fixer):
    dquote_codepoints = {k for k, v in fixer.codepoint_map.items() if v == '"'}
    squote_codepoints = {k for k, v in fixer.codepoint_map.items() if v == "'"}
    return (dquote_codepoints, squote_codepoints)


def test_fix_ligatures_arg_parsing():
    args1 = LIGATURE_FIXER._parse_args(argv=["foo", "bar"])
    assert list(args1.files) == ["foo", "bar"]
    assert args1.show_changes is False

    args2 = LIGATURE_FIXER._parse_args(argv=["foo", "--show-changes"])
    assert list(args2.files) == ["foo"]
    assert args2.show_changes is True


def test_fix_smartquotes_arg_parsing():
    fixer = QuoteFixer()
    args1 = fixer._parse_args(argv=["foo", "bar"])
    assert list(args1.files) == ["foo", "bar"]
    assert args1.show_changes is False
    assert _extra_quote_codepoints(fixer) == (
        set(DEFAULT_DOUBLE_QUOTE_CODEPOINTS),
        set(DEFAULT_SINGLE_QUOTE_CODEPOINTS),
    )

    fixer = QuoteFixer()
    args2 = fixer._parse_args(argv=["foo", "--show-changes"])
    assert list(args2.files) == ["foo"]
    assert args2.show_changes is True
    assert _extra_quote_codepoints(fixer) == (
        set(DEFAULT_DOUBLE_QUOTE_CODEPOINTS),
        set(DEFAULT_SINGLE_QUOTE_CODEPOINTS),
    )

    fixer = QuoteFixer()
    args3 = fixer._parse_args(argv=["foo", "--double-quote-codepoints", "FF02,201C"])
    assert list(args3.files) == ["foo"]
    assert args3.show_changes is False
    assert _extra_quote_codepoints(fixer) == (
        {"FF02", "201C"},
        set(DEFAULT_SINGLE_QUOTE_CODEPOINTS),
    )

    fixer = QuoteFixer()
    args4 = fixer._parse_args(argv=["foo", "--single-quote-codepoints", "FF07,201B"])
    assert list(args4.files) == ["foo"]
    assert args4.show_changes is False
    assert _extra_quote_codepoints(fixer) == (
        set(DEFAULT_DOUBLE_QUOTE_CODEPOINTS),
        {"FF07", "201B"},
    )


@pytest.mark.parametrize("fixer", [LIGATURE_FIXER, QuoteFixer()])
def test_invalid_color_opt(fixer):
    with pytest.raises(SystemExit) as excinfo:
        fixer._parse_args(argv=["foo", "--color", "bar"])
    err = excinfo.value
    assert err.code == 2
