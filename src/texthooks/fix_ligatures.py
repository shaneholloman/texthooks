"""
A fixer script which crawls text files and replaces Unicode Ligatures with
non-ligature (mostly ASCII) two-character representations.

This intentionally limits itself to ligatures which are no semantically different from
the non-ligature representations (e.g. 'ff' vs 'U+FB00'). The reason being that
the fixers is intended to fix text which has been ligature-ized for
presentation (e.g. by LaTeX) but was originally input as ASCII-friendly latin
text.
"""

from ._fixer_core import CodepointFixer

# map unicode codepoints to non-ligature versions of those chars
CODEPOINT_MAP = {
    "FB00": "ff",
    "FB01": "fi",
    "FB02": "fl",
    "FB03": "ffi",
    "FB04": "ffl",
}

main = CodepointFixer.script_main(__doc__, CODEPOINT_MAP)
if __name__ == "__main__":
    main()
