"""A game of chess."""

from pathlib import Path

from pkg_resources import get_distribution

__version__ = get_distribution("consolechess").version

__WORKING_DIRECTORY__ = Path(
    Path(__file__).parent if "__file__" in globals() else "consolechess"
)
