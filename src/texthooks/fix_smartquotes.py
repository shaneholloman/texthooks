#!/usr/bin/env python3
"""
A fixer script which crawls text files and replaces smartquotes with
normal quote characters.
This fixes copy-paste from some applications which replace double-quotes with
curly quotes.

For extra credit, it handles alternate encodings of quotation marks and
dingbats.

It does *not* convert corner brackets, braile quotation marks, or angle
quotation marks. Those characters are not typically the result of copy-paste
errors, so they are allowed.

Low quotation marks vary in usage and meaning by language, and some languages
use quotation marks which are facing "outwards" (opposite facing from english).
For the most part, these and exotic characters (double-prime quotes) are
ignored.

In files with the offending marks, they are replaced and the run is marked as
failed. This makes the script suitable as a pre-commit fixer.
"""

import argparse
import sys
import typing as t

from ._fixer_core import CodepointFixer

# lists of unicode codepoints, commented with their unicode names
DEFAULT_DOUBLE_QUOTE_CODEPOINTS = (
    # STRAIGHT DOUBLE QUOTES
    "0022",  # Quotation mark
    "FF02",  # Fullwidth quotation mark
    # LEFT DOUBLE QUOTES
    "201C",  # Left double quotation mark
    "201F",  # Double high-reversed-9 quotation mark
    "275D",  # Heavy double turned comma quotation mark ornament
    "1F676",  # Sans-serif heavy double turned comma quotation mark ornament
    # RIGHT DOUBLE QUOTES
    "201D",  # Right double quotation mark
    "275E",  # Heavy double comma quotation mark ornament
    "1F677",  # Sans-serif heavy double comma quotation mark ornament
)
DEFAULT_SINGLE_QUOTE_CODEPOINTS = (
    # STRAIGHT SINGLE QUOTES
    "0027",  # Apostrophe
    "FF07",  # Fullwidth apostrophe
    # LEFT SINGLE QUOTES
    "2018",  # Left single quotation mark
    "201B",  # Single high-reversed-9 quotation mark
    "275B",  # Heavy single turned comma quotation mark ornament
    # RIGHT SINGLE QUOTES
    "2019",  # Right single quotation mark
    "275C",  # Heavy single comma quotation mark ornament
)


class QuoteFixer(CodepointFixer):
    def modify_cli_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--double-quote-codepoints",
            type=str,
            help=(
                "A comma-delimited list of unicode codepoints for characters "
                "which should be treated as double quotes. "
                f"default: {','.join(DEFAULT_DOUBLE_QUOTE_CODEPOINTS)}"
            ),
        )
        parser.add_argument(
            "--single-quote-codepoints",
            type=str,
            help=(
                "A comma-delimited list of unicode codepoints for characters "
                "which should be treated as single quotes. "
                f"default: {','.join(DEFAULT_SINGLE_QUOTE_CODEPOINTS)}"
            ),
        )

    def postprocess_cli_args(self, args: argparse.Namespace) -> argparse.Namespace:
        double_quote_is_set = self.map_comma_delimited_arg(
            args.double_quote_codepoints, DEFAULT_DOUBLE_QUOTE_CODEPOINTS, '"'
        )
        single_quote_is_set = self.map_comma_delimited_arg(
            args.single_quote_codepoints, DEFAULT_SINGLE_QUOTE_CODEPOINTS, "'"
        )
        if not (double_quote_is_set or single_quote_is_set):
            print(
                "fix-smartquotes cannot run when both sets of codepoints are empty.",
                file=sys.stderr,
            )
            raise SystemExit(2)

        return args


def main(*, argv: list[str] | None = None) -> t.NoReturn:
    fixer = QuoteFixer(__doc__)
    raise SystemExit(fixer.main(argv=argv))


if __name__ == "__main__":
    main()
