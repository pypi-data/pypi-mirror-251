"""Utilities for managing PGN files and opening books."""

import re
from collections.abc import Iterable, Iterator
from datetime import datetime
from pathlib import Path

from .board import OpeningTree


def get_pgn_field_by_name(pgn: str, name: str) -> str | None:
    """Get PGN field by field name and PGN text."""
    return mat.group(1) if (mat := re.search(rf"\[{name} \"(.+?)\"\]", pgn)) else None


def pgn_database_to_dicts(path: Path | str) -> list[dict[str, int | str | None]]:
    """Read a .pgn file to a list of dicts."""
    return [
        {
            "game_no": i,
            "variant": get_pgn_field_by_name(pgn, "Variant"),
            "imported_pgn": pgn,
            "imported_bare_moves": strip_bare_moves_from_pgn(pgn),
            "imported_result": get_pgn_field_by_name(pgn, "Result"),
            "imported_termination": get_pgn_field_by_name(pgn, "Termination"),
            "imported_initial_fen": get_pgn_field_by_name(pgn, "FEN"),
        }
        for i, pgn in enumerate(iter_pgn_file(path))
    ]


def make_openings_tree(openings: list[dict[str, str]]) -> OpeningTree:
    """
    Create a tree of dicts from a list of opening dicts with 'eco', 'name', and
    'moves' keys.
    """
    tree: OpeningTree = {}
    for opening in openings:
        if "bare_moves" not in opening:
            opening.update(
                {
                    "bare_moves": re.sub(
                        r"\d+\.+\s*",
                        "",
                        opening["moves"],  # type: ignore
                    ).split()
                }
            )
        index_chain = []
        cursor = tree
        for move in opening["bare_moves"][:-1]:
            index_chain.append(move)
            if move not in cursor:
                cursor[move] = {}  # type: ignore
            cursor = cursor[move]  # type: ignore
        last_move = opening["bare_moves"][-1]
        if last_move not in cursor:
            cursor[last_move] = {}  # type: ignore
        cursor[last_move]["null"] = {  # type: ignore
            key: opening[key] for key in opening if key != "bare_moves"
        }
    return tree


def read_pgn_file(path: Path | str) -> list[str]:
    """Read a .pgn file to a list of PGN strings."""
    with Path(path).open() as file:
        text = file.read()
    return [f"[{pgn}" for pgn in text.split("\n\n[") if len(pgn) > 0 and pgn[0] != "["]


def write_pgn_file(
    pgns: Iterable[str], path: Path | str, *, overwrite: bool = False
) -> None:
    """Write a PGN file from a sequence of PGN strings."""
    path = Path(path)
    exception: Exception | None = None
    with path.open("w" if overwrite else "x") as file:
        try:
            file.write("\n".join(pgns))
        except Exception as exc:
            exception = exc
    if exception is None:
        return None
    elif not overwrite:
        path.unlink(missing_ok=True)
    raise exception


def iter_pgn_file(db: Path | str) -> Iterator[str]:
    """Iterate through PGN strings in file."""
    output = ""
    with Path(db).open() as file:
        for line in file:
            if output != "" and "[Event " in line:
                yield re.sub(r"\n+$", "\n", output)
                output = ""
            output += line


def strip_bare_moves_from_pgn(pgn: str, *, strip_numbers: bool = True) -> str:
    """Strip the SAN tokens from a PGN string."""
    pattern = (
        r"\[.+?\]|\{.+?\}|\d+\.+|[10]-[10]|\*|1/2-1/2|[?!]"
        if strip_numbers
        else r"\[.+?\]|\{.+?\}|[10]-[10]|\*|1/2-1/2|[?!]"
    )
    return re.sub(r"[\n\s]+", " ", re.sub(pattern, "", pgn)).replace("P@", "@").strip()


def moves_list_from_pgn(pgn: str) -> list[str]:
    """Get list of SAN tokens from a PGN string."""
    return re.sub(r"\[.+?\]|\{.+?\}|\d+\.+|[10]-[10]|\*|1/2-1/2|[?!]", "", pgn).split()


def date_to_pgn_format(date: datetime) -> str:
    """Convert a date into a PGN format string (YYYY-MM-DD)."""
    return date.strftime("%Y.%m.%d")
