"""
A fixer script which crawls text files and replaces Unicode Ligatures with
non-ligature (mostly ASCII) two-character representations.

This intentionally limits itself to ligatures which are no semantically different from
the non-ligature representations (e.g. 'ff' vs 'U+FB00'). The reason being that
the fixers is intended to fix text which has been ligature-ized for
presentation (e.g. by LaTeX) but was originally input as ASCII-friendly latin
text.
"""

import typing as t

from ._fixer_core import CodepointFixer

# map unicode codepoints to non-ligature versions of those chars
CODEPOINT_MAP = {
    "FB00": "ff",
    "FB01": "fi",
    "FB02": "fl",
    "FB03": "ffi",
    "FB04": "ffl",
}


LIGATURE_FIXER = CodepointFixer(__doc__, CODEPOINT_MAP)


def main(*, argv: list[str] | None = None) -> t.NoReturn:
    raise SystemExit(LIGATURE_FIXER.main(argv=argv))


if __name__ == "__main__":
    main()
