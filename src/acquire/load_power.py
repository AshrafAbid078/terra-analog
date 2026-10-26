
"""
NASA POWER climate data loader for Terra Analog.

Reads manually downloaded CSV files from:
    data/raw/power/

Supports NASA POWER climatology CSVs with metadata followed by a table:
    PARAMETER,JAN,FEB,...,DEC,ANN

Writes:
    cache/power_climatology.csv

No live API calls are made.
"""

from pathlib import Path
import re
import warnings

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "power"
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_FILE = CACHE_DIR / "power_climatology.csv"

MONTHS = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
]


def find_parameter_table(file_path):
    """Find the line where the NASA POWER parameter table begins."""
    with file_path.open("r", encoding="utf-8-sig", errors="replace") as file:
        for line_number, line in enumerate(file):
            columns = [part.strip().upper() for part in line.strip().split(",")]

            if columns and columns[0] == "PARAMETER" and "ANN" in columns:
                return line_number

    return None


def read_metadata(file_path):
    """Extract latitude and longitude from NASA POWER metadata."""
    metadata = {
        "latitude": None,
        "longitude": None,
    }

    with file_path.open("r", encoding="utf-8-sig", errors="replace") as file:
        text = file.read(20000)

    patterns = {
        "latitude": r"Latitude\s*[:=]?\s*(-?\d+(?:\.\d+)?)",
        "longitude": r"Longitude\s*[:=]?\s*(-?\d+(?:\.\d+)?)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            metadata[key] = float(match.group(1))

    return metadata


def read_power_csv(file_path):
    """Read a NASA POWER climatology table, skipping preceding metadata."""
    table_line = find_parameter_table(file_path)

    if table_line is None:
        return None

    try:
        table = pd.read_csv(file_path, skiprows=table_line)
    except (OSError, pd.errors.ParserError, UnicodeError) as exc:
        warnings.warn(f"Could not read {file_path.name}: {exc}")
        return None

    if "PARAMETER" not in table.columns:
        return None

    table["PARAMETER"] = table["PARAMETER"].astype(str).str.strip().str.upper()
    table = table.drop_duplicates(subset="PARAMETER", keep="last")
    table = table.set_index("PARAMETER")

    # Convert numeric values and replace NASA's missing-value marker.
    table = table.apply(pd.to_numeric, errors="coerce")
    table = table.replace(-999, float("nan"))

    return table


def get_annual_value(table, parameter):
    """Get a parameter's annual value if available."""
    if parameter not in table.index or "ANN" not in table.columns:
        return None

    value = table.at[parameter, "ANN"]

    if pd.isna(value):
        return None

    return float(value)


def get_temperature_range(table):
    """
    Return the annual climatological daily temperature range in °C.

    Prefer NASA POWER's T2M_RANGE annual value. If unavailable,
    estimate it from monthly T2M_MAX minus T2M_MIN.
    """
    direct_value = get_annual_value(table, "T2M_RANGE")

    if direct_value is not None:
        return direct_value

    if "T2M_MAX" not in table.index or "T2M_MIN" not in table.index:
        return None

    available_months = [
        month for month in MONTHS
        if month in table.columns
        and pd.notna(table.at["T2M_MAX", month])
        and pd.notna(table.at["T2M_MIN", month])
    ]

    if not available_months:
        return None

    differences = [
        float(table.at["T2M_MAX", month])
        - float(table.at["T2M_MIN", month])
        for month in available_months
    ]

    return sum(differences) / len(differences)


def process_file(file_path):
    """Convert one NASA POWER climatology file into a normalized record."""
    table = read_power_csv(file_path)

    # Skip location catalogues and CSVs that lack a POWER parameter table.
    if table is None:
        return None

    metadata = read_metadata(file_path)

    precipitation = get_annual_value(table, "PRECTOTCORR")
    temperature = get_annual_value(table, "T2M")
    temperature_range = get_temperature_range(table)

    # A valid aridity index requires precipitation and potential
    # evapotranspiration (PET). Do not substitute rainfall alone.
    pet = get_annual_value(table, "PET")
    aridity = None

    if precipitation is not None and pet is not None and pet > 0:
        aridity = precipitation * 365.0 / pet

    if aridity is None:
        warnings.warn(
            f"{file_path.name}: aridity not calculated; "
            "a compatible PET variable is not available."
        )

    return {
        "location": file_path.stem,
        "latitude": metadata["latitude"],
        "longitude": metadata["longitude"],
        "temp_range_c": temperature_range,
        "aridity": aridity,
        "precipitation_mm_day": precipitation,
        "annual_mean_temp_c": temperature,
        "source_file": file_path.name,
    }


def load_power():
    """Load all supported local POWER climatology CSVs and save the result."""
    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"Raw POWER folder not found: {RAW_DIR}\n"
            "Create data/raw/power/ and put your downloaded files there."
        )

    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DIR}")

    records = []

    for file_path in csv_files:
        try:
            record = process_file(file_path)
            if record is not None:
                records.append(record)
                print(f"Loaded: {file_path.name}")
            else:
                print(f"Skipped (no climatology table): {file_path.name}")
        except (OSError, ValueError, KeyError, pd.errors.ParserError) as exc:
            warnings.warn(f"Skipped {file_path.name}: {exc}")

    if not records:
        raise ValueError(
            "No supported NASA POWER climatology tables were found. "
            "Check the downloaded CSV files and their formats."
        )

    result = pd.DataFrame(records)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"\nProcessed {len(result)} location(s).")
    print(f"Saved output to: {OUTPUT_FILE}")

    return result


if __name__ == "__main__":
    result = load_power()
    print("\nPreview:")
    print(result.to_string(index=False))

