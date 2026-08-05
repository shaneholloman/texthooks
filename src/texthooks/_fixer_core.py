import argparse
import functools
import re
import typing as t

from ._common import all_filenames, codepoint2char, parse_cli_args
from ._recorders import DiffRecorder


class CodepointFixer:
    def __init__(
        self,
        docstring: str,
        seed_codepoint_map: t.Mapping[str, str] | t.Iterable[tuple[str, str]] = (),
    ) -> None:
        self.docstring = docstring
        self.codepoint_map = CodepointMap(seed_codepoint_map)

    def main(self, *, argv: list[str] | None = None) -> int:
        args = self._parse_args(argv=argv)
        changes = self._do_replacements(args)

        if changes:
            changes.print_changes(
                args.show_changes,
                args.color,
                charwidth=self.codepoint_map.get_mapped_width,
            )

        return 1 if changes else 0

    def _parse_args(self, argv: list[str] | None) -> argparse.Namespace:
        return parse_cli_args(
            self.docstring,
            argv=argv,
            modify_parser=self.modify_cli_parser,
            postprocess=self.postprocess_cli_args,
            fixer=True,
        )

    def modify_cli_parser(self, parser: argparse.ArgumentParser) -> None:
        """Overrideable hook."""

    def postprocess_cli_args(self, args: argparse.Namespace) -> argparse.Namespace:
        """Overrideable hook."""
        return args

    def map_comma_delimited_arg(
        self, arg_value: str | None, default: t.Iterable[str], value: str
    ) -> bool:
        """
        Add a comma-delimited arg value to the codepoint map, falling back to a default
        expressed as an iterable.

        Returns False if the value was cleared (empty), True otherwise.
        """
        if arg_value == "":
            return False

        if arg_value is None:
            source = default
        else:
            source = arg_value.split(",")

        self.codepoint_map.update(dict.fromkeys(source, value))
        return True

    def _do_replacements(self, args: argparse.Namespace) -> DiffRecorder:
        recorder = DiffRecorder(args.verbosity, check=args.check)
        for fn in all_filenames(args.files):
            recorder.run_line_fixer(self.codepoint_map.translate_line, fn)
        return recorder


class CodepointMap(dict[str, str]):
    def get_mapped_width(self, c: str) -> int:
        return len(self.get(c, c))

    @functools.cached_property
    def replacement_pattern(self) -> re.Pattern:
        return re.compile("(" + "|".join(self.charmap.keys()) + ")")

    @functools.cached_property
    def charmap(self) -> dict[str, str]:
        return {  # remap in terms of chars
            codepoint2char(k): v for k, v in self.items()
        }

    def translate_line(self, line: str) -> str:
        return self.replacement_pattern.sub(self._sub_char, line)

    def _sub_char(self, match: re.Match) -> str:
        c = match.group(0)
        return self.charmap.get(c, c)

    def _clear_caches(self) -> None:
        if hasattr(self, "replacement_pattern"):
            del self.replacement_pattern
        if hasattr(self, "charmap"):
            del self.charmap

    def __setitem__(self, k: str, v: str) -> None:
        super().__setitem__(k, v)
        self._clear_caches()

    def __delitem__(self, v: str) -> None:
        super().__delitem__(v)
        self._clear_caches()

    # don't support all of the superclass usages; override with just mapping support
    def update(self, m: t.Mapping[str, str]) -> None:  # type: ignore[override]
        super().update(m)
        self._clear_caches()

    def clear(self) -> None:
        super().clear()
        self._clear_caches()
