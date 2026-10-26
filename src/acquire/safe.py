
"""Safe data loading for Terra Analog.

Loading order:
1. Used a valid cached output.
2. Fall back to an existing demo fixture.
3. Return None if neither source is usable.

 module never downloads data or invents replacement values.
"""

from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

# Project root: terra-analog/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CACHE_DIR = PROJECT_ROOT / "cache"
FIXTURES_DIR = PROJECT_ROOT / "demo fixtures"


def _is_usable(path: Path) -> bool:
    """Return True if the path exists and contains readable, non-empty data."""
    try:
        if not path.is_file() or path.stat().st_size == 0:
            return False

        # Check JSON cache files for valid JSON.
        if path.suffix.lower() == ".json":
            with path.open("r", encoding="utf-8") as file:
                json.load(file)

        return True

    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        logger.warning("Data file is not usable: %s (%s)", path, exc)
        return False


def load_cached_or_fixture(
    cache_path: str | Path,
    fixture_path: str | Path,
) -> Path | None:
    """Return the cache path first, or a fixture path if the cache is unusable.

    Absolute paths are used as supplied. Relative paths are resolved from
    the project root.

    Returns:
        Path: The first usable file.
        None: If neither file is usable.
    """

    cache = Path(cache_path)
    fixture = Path(fixture_path)

    if not cache.is_absolute():
        cache = PROJECT_ROOT / cache

    if not fixture.is_absolute():
        fixture = PROJECT_ROOT / fixture

    if _is_usable(cache):
        logger.info("Using cached data: %s", cache)
        return cache

    logger.warning("Cache unavailable; trying demo fixture: %s", fixture)

    if _is_usable(fixture):
        logger.info("Using demo fixture: %s", fixture)
        return fixture

    logger.error(
        "No usable cache or fixture found. Cache: %s | Fixture: %s",
        cache,
        fixture,
    )
    return None


def load_json_cached_or_fixture(
    cache_path: str | Path,
    fixture_path: str | Path,
) -> dict | list | None:
    """Load JSON data from cache, falling back to a JSON fixture."""

    selected_path = load_cached_or_fixture(cache_path, fixture_path)

    if selected_path is None:
        return None

    try:
        with selected_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        logger.warning("Could not read JSON file %s: %s", selected_path, exc)
        return None

