#!/usr/bin/env python3
"""
A fixer script which crawls text files and replaces Unicode dash characters
with ASCII equivalents.

This normalizes various dash, and minus signs to single hyphens, and
treats several longer dashes like the em dash as double-hyphens.

A variety of language-specific hyphen-like marks, like the Japanese long sound
mark (U+30FC), are ignored.

In files with the offending characters, they are replaced and the run is
marked as failed. This makes the script suitable as a pre-commit fixer.
"""

import argparse
import sys
import typing as t

from ._fixer_core import CodepointFixer

# Unicode codepoints for dash characters, commented with their unicode names
DEFAULT_SINGLE_HYPHEN_CODEPOINTS = (
    # hyphens
    "2010",  # Hyphen
    "2011",  # Non-Breaking Hyphen
    "FE63",  # Small Hyphen-Minus
    # standalone punctuation
    "2012",  # Figure Dash
    "2013",  # En Dash
    # minus signs
    "2212",  # Minus Sign
    "02D7",  # Modifier Letter Minus Sign
    "2796",  # Heavy Minus Sign
)

# Unicode codepoints for long-dash characters, commented with their unicode names
DEFAULT_DOUBLE_HYPHEN_CODEPOINTS = (
    # wide hyphens
    "FF0D",  # Fullwidth Hyphen-Minus
    # standalone long-dash punctuation
    "2014",  # Em Dash
    "FE58",  # Small Em Dash
)


class DashFixer(CodepointFixer):
    def modify_cli_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--single-hyphen-codepoints",
            type=str,
            help=(
                "A comma-delimited list of unicode codepoints for characters "
                "which should be replaced with single hyphens. "
                f"default: {','.join(DEFAULT_SINGLE_HYPHEN_CODEPOINTS)}"
            ),
        )
        parser.add_argument(
            "--double-hyphen-codepoints",
            type=str,
            help=(
                "A comma-delimited list of unicode codepoints for characters "
                "which should be replaced with double hyphens. "
                f"default: {','.join(DEFAULT_DOUBLE_HYPHEN_CODEPOINTS)}"
            ),
        )

    def postprocess_cli_args(self, args: t.Any) -> t.Any:
        # convert comma delimited lists manually
        if args.single_hyphen_codepoints is None:
            args.single_hyphen_codepoints = DEFAULT_SINGLE_HYPHEN_CODEPOINTS
        elif args.single_hyphen_codepoints == "":
            args.single_hyphen_codepoints = []
        else:
            args.single_hyphen_codepoints = args.hyphen_codepoints.split(",")

        if args.double_hyphen_codepoints is None:
            args.double_hyphen_codepoints = DEFAULT_DOUBLE_HYPHEN_CODEPOINTS
        elif args.double_hyphen_codepoints == "":
            args.double_hyphen_codepoints = []
        else:
            args.double_hyphen_codepoints = args.double_hyphen_codepoints.split(",")

        if not (
            bool(args.single_hyphen_codepoints) or bool(args.double_hyphen_codepoints)
        ):
            print(
                "fix-unicode-dashes cannot run when both sets of codepoints are empty.",
                file=sys.stderr,
            )
            raise SystemExit(2)

        self.codepoint_map.update(
            dict.fromkeys(args.single_hyphen_codepoints, "-")
            | dict.fromkeys(args.double_hyphen_codepoints, "--")
        )

        return args


def main(*, argv: list[str] | None = None) -> t.NoReturn:
    fixer = DashFixer(__doc__)
    raise SystemExit(fixer.main(argv=argv))


if __name__ == "__main__":
    main()
