"""
A fixer script which crawls text files and replaces various unicode space
separators with the space character.

This normalizes No-Break Space and similar characters to ensure that your files
render the same way in all contexts. It does not modify newlines, carriage returns, or
other whitespace characters outside of the Space Separator category.

Of the various space separators, only U1680 (Ogham Space Mark) is typically represented
in a visually distinct way, and is therefore ignored.

In files with the offending characters, they are replaced and the run is marked as
failed. This makes the script suitable as a pre-commit fixer.
"""

import argparse
import sys

from ._fixer_core import CodepointFixer

# lists of unicode codepoints, commented with their unicode names
DEFAULT_SEPARATOR_CODEPOINTS = (
    # non-breaking
    "00A0",  # No-Break Space
    "202F",  # Narrow No-Break Space
    # various sized spaces
    "2000",  # En Quad
    "2001",  # Em Quad
    "2002",  # En Space
    "2003",  # Em Space
    "2004",  # Three-Per-Em Space
    "2005",  # Four-Per-Em Space
    "2006",  # Six-Per-Em Space
    "2007",  # Figure Space
    "2008",  # Punctuation Space
    "2009",  # Thin Space
    "200A",  # Hair Space
    # other...
    "205F",  # Medium Mathematical Space
    "3000",  # Ideographic Space
)


class SpaceFixer(CodepointFixer):
    def modify_cli_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--separator-codepoints",
            type=str,
            help=(
                "A comma-delimited list of unicode codepoints for characters "
                "which should be treated as single quotes. "
                f"default: {','.join(DEFAULT_SEPARATOR_CODEPOINTS)}"
            ),
        )

    def postprocess_cli_args(self, args: argparse.Namespace) -> argparse.Namespace:
        if not self.map_comma_delimited_arg(
            args.separator_codepoints, DEFAULT_SEPARATOR_CODEPOINTS, " "
        ):
            print(
                "fix-spaces cannot run when the set of codepoints is empty.",
                file=sys.stderr,
            )
            raise SystemExit(2)
        return args


main = SpaceFixer.script_main(__doc__)
if __name__ == "__main__":
    main()
