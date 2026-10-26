
"""DEM loader for Terra Analog.

Reads manually downloaded SRTM HGT and GeoTIFF elevation files from:
    data/raw/dem/

Derives:
    elevation_m
    slope_deg
    roughness

Writes normalized GeoTIFF layers to:
    cache/dem/

No live API calls are made.
"""

from pathlib import Path
import warnings

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "dem"
CACHE_DIR = PROJECT_ROOT / "cache" / "dem"


def find_dem_files():
    """Find HGT and GeoTIFF files recursively."""
    supported = {".hgt", ".tif", ".tiff"}
    return sorted(
        path for path in RAW_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in supported
    )


def read_elevation(file_path):
    """Read elevation data and spatial metadata."""
    with rasterio.open(file_path) as src:
        elevation = src.read(1, masked=True).astype("float32")
        crs = src.crs

        if crs is None and file_path.suffix.lower() == ".hgt":
            crs = rasterio.crs.CRS.from_epsg(4326)
        elif crs is None:
            raise ValueError("Raster has no coordinate reference system.")

        transform = src.transform
        nodata = src.nodata
        elevation = elevation.filled(np.nan)

        if nodata is not None:
            elevation[elevation == nodata] = np.nan

        if file_path.suffix.lower() == ".hgt":
            elevation[elevation <= -32768] = np.nan

        if not np.any(np.isfinite(elevation)):
            raise ValueError("No valid elevation pixels found.")

        return elevation, transform, crs


def reproject_to_geographic(elevation, transform, source_crs):
    """Reproject to WGS84 without forcing a coarse 0.5-degree resolution."""
    height, width = elevation.shape
    bounds = rasterio.transform.array_bounds(
        height, width, transform
    )

    dst_transform, dst_width, dst_height = calculate_default_transform(
        source_crs,
        "EPSG:4326",
        width,
        height,
        *bounds,
    )

    destination = np.full(
        (dst_height, dst_width),
        np.nan,
        dtype=np.float32,
    )

    reproject(
        source=elevation,
        destination=destination,
        src_transform=transform,
        src_crs=source_crs,
        src_nodata=np.nan,
        dst_transform=dst_transform,
        dst_crs="EPSG:4326",
        dst_nodata=np.nan,
        resampling=Resampling.bilinear,
    )

    if not np.any(np.isfinite(destination)):
        raise ValueError("Reprojection produced no valid elevation pixels.")

    return destination, dst_transform


def calculate_terrain_layers(elevation, transform):
    """Calculate elevation, slope in degrees, and local roughness."""
    elevation = np.asarray(elevation, dtype=np.float32)
    valid = np.isfinite(elevation)

    if not np.any(valid):
        raise ValueError("No valid elevation values available.")

    rows, cols = elevation.shape

    if rows < 2 or cols < 2:
        raise ValueError(
            f"Raster is too small for slope calculation: {cols} x {rows}"
        )

    pixel_height_degrees = abs(transform.e)
    pixel_width_degrees = abs(transform.a)

    if pixel_height_degrees == 0 or pixel_width_degrees == 0:
        raise ValueError("Raster transform has invalid pixel dimensions.")

    row_indices = np.arange(rows)
    latitude = transform.f + (row_indices + 0.5) * transform.e

    # Approximate pixel distances in metres.
    dy = pixel_height_degrees * 111320.0
    dx = np.maximum(
        pixel_width_degrees * 111320.0
        * np.abs(np.cos(np.radians(latitude))),
        1.0,
    )

    # Fill missing cells temporarily for gradient calculation.
    median_elevation = float(np.nanmedian(elevation))
    work = np.where(valid, elevation, median_elevation)

    gradient_y, gradient_x = np.gradient(work)
    gradient_y = gradient_y / dy
    gradient_x = gradient_x / dx[:, None]

    slope = np.degrees(
        np.arctan(np.sqrt(gradient_x**2 + gradient_y**2))
    )

    # Local 3 x 3 standard deviation in metres.
    padded = np.pad(work, 1, mode="edge")
    neighbours = np.stack(
        [
            padded[i:i + rows, j:j + cols]
            for i in range(3)
            for j in range(3)
        ],
        axis=0,
    )
    roughness = np.std(neighbours, axis=0)

    slope[~valid] = np.nan
    roughness[~valid] = np.nan

    return (
        elevation,
        slope.astype(np.float32),
        roughness.astype(np.float32),
    )


def save_raster(path, data, transform, crs="EPSG:4326"):
    """Save one terrain layer as a GeoTIFF."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype="float32",
        crs=crs,
        transform=transform,
        nodata=np.nan,
        compress="deflate",
    ) as dst:
        dst.write(data.astype(np.float32), 1)


def load_dem():
    """Process available HGT and GeoTIFF elevation files."""
    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"DEM folder not found: {RAW_DIR}"
        )

    files = find_dem_files()
    if not files:
        raise FileNotFoundError(
            f"No .hgt, .tif, or .tiff files found in {RAW_DIR}"
        )

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    processed = []

    for file_path in files:
        try:
            print(f"Processing: {file_path.name}")

            elevation, transform, crs = read_elevation(file_path)

            geographic, geographic_transform = reproject_to_geographic(
                elevation, transform, crs
            )

            elevation_layer, slope_layer, roughness_layer = (
                calculate_terrain_layers(
                    geographic, geographic_transform
                )
            )

            stem = file_path.stem
            outputs = {
                f"{stem}_elevation_m.tif": elevation_layer,
                f"{stem}_slope_deg.tif": slope_layer,
                f"{stem}_roughness.tif": roughness_layer,
            }

            for filename, layer in outputs.items():
                save_raster(
                    CACHE_DIR / filename,
                    layer,
                    geographic_transform,
                )

            processed.append(file_path.name)
            print(
                f"Saved terrain layers for {file_path.name} "
                f"({geographic.shape[1]} x {geographic.shape[0]} pixels)"
            )

        except (OSError, ValueError, rasterio.errors.RasterioError) as exc:
            warnings.warn(
                f"Could not process {file_path.name}: {exc}"
            )

    if not processed:
        raise ValueError(
            "No DEM files could be processed. Check the input files "
            "and confirm rasterio can read them."
        )

    print(f"\nProcessed {len(processed)} DEM file(s).")
    print(f"Output directory: {CACHE_DIR}")

    return processed


if __name__ == "__main__":
    load_dem()


