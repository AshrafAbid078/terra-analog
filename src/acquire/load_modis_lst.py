
""" a surface-temperature-range proxy from NASA POWER CSV files.

Important:
- This is a NASA POWER surface-temperature proxy, not MODIS LST.
- TS_MAX and TS_MIN are used when both are available.
- Missing or invalid values are not invented.
- Output is written to cache/modis_lst/ for compatibility with the project.
"""

from pathlib import Path
import csv
import math
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
POWER_DIR = PROJECT_ROOT / "data" / "raw" / "power"
OUTPUT_DIR = PROJECT_ROOT / "cache" / "modis_lst"
OUTPUT_FILE = OUTPUT_DIR / "surface_temp_range_proxy.csv"


def read_power_csv(path: Path) -> dict:
    """Read NASA POWER's parameter/month/value table."""
    parameters = {}

    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue

            parameter = row[0].strip().upper()

            # Ignore metadata and header rows.
            if parameter in {"PARAMETER", "YEAR", "ANN"}:
                continue

            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", parameter):
                continue

            values = []
            for cell in row[1:]:
                try:
                    value = float(cell.strip())
                    if not math.isfinite(value) or value <= -900:
                        value = None
                except (ValueError, AttributeError):
                    value = None
                values.append(value)

            # A parameter row should have at least some numeric values.
            if any(value is not None for value in values):
                parameters[parameter] = values

    return parameters


def monthly_ranges(parameters: dict) -> list:
    """Calculate monthly surface-temperature ranges where possible."""
    maximum = parameters.get("TS_MAX")
    minimum = parameters.get("TS_MIN")

    if not maximum or not minimum:
        return []

    # The first 12 entries are Jan-Dec; a possible 13th is ANN.
    ranges = []
    for index in range(min(12, len(maximum), len(minimum))):
        high = maximum[index]
        low = minimum[index]

        if high is None or low is None:
            ranges.append(None)
        else:
            ranges.append(round(high - low, 3))

    return ranges


def main():
    if not POWER_DIR.exists():
        raise FileNotFoundError(f"NASA POWER folder not found: {POWER_DIR}")

    files = sorted(
        path for path in POWER_DIR.glob("*.csv")
        if path.is_file()
    )

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in {POWER_DIR}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    output_rows = []

    for path in files:
        # Skip unrelated or combined files if they lack the required variables.
        parameters = read_power_csv(path)
        ranges = monthly_ranges(parameters)

        if not ranges:
            print(f"SKIPPED (no TS_MAX/TS_MIN): {path.name}")
            continue

        valid_ranges = [value for value in ranges if value is not None]
        annual_mean = (
            round(sum(valid_ranges) / len(valid_ranges), 3)
            if valid_ranges else None
        )

        row = {
            "source_file": path.name,
            "source": "NASA POWER",
            "criterion": "surface_temp_range_proxy_c",
            "is_modis_observation": False,
            "annual_mean_monthly_range_c": annual_mean,
        }

        for month, value in zip(months, ranges):
            row[f"{month.lower()}_range_c"] = value

        output_rows.append(row)
        print(f"Processed: {path.name}")

    if not output_rows:
        raise ValueError(
            "No usable files found. Confirm that the NASA POWER CSVs "
            "contain TS_MAX and TS_MIN rows."
        )

    fieldnames = list(output_rows[0].keys())

    with OUTPUT_FILE.open(
        "w", encoding="utf-8", newline=""
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nSaved {len(output_rows)} records to:")
    print(OUTPUT_FILE)
    print(
        "\nNote: These are NASA POWER surface-temperature-range proxies, "
        "not verified MODIS daytime/nighttime LST measurements."
    )


if __name__ == "__main__":
    main()


