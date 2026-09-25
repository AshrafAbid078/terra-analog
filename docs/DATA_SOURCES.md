# DATA_SOURCES.md
## Terra Analog — Source Citation Log

This document serves as the master list of all raw datasets used in this project. All data cited here is stored in `data/raw/` and processed locally.

---

### 1. Earth Climate & Atmosphere (POWER)
* **Description:** Solar and meteorological data on a global grid (aridity, temperature range).
* **Source:** NASA POWER Data Access Viewer / REST API
* **URLs:** 
  - https://power.larc.nasa.gov/data-access-viewer/
  - https://power.larc.nasa.gov/docs/services/api/
* **Accessed:** September 2026

### 2. Earth Topography & DEM
* **Description:** Global NASADEM and SRTM elevation tiles (elevation, slope, roughness).
* **Source:** NASA Earthdata Search / ASF / USGS 3DEP
* **URLs:**
  - https://search.earthdata.nasa.gov/
  - https://search.asf.alaska.edu/#/
  - https://apps.nationalmap.gov/downloader/
  - https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html
* **Accessed:** September 2026

### 3. Earth Thermal Dynamics (MODIS/VIIRS)
* **Description:** Daily Land Surface Temperature (diurnal temperature range).
* **Source:** NASA Worldview / AppEEARS / LP DAAC MODIS MOD11A1
* **URLs:**
  - https://worldview.earthdata.nasa.gov/
  - https://appeears.earthdatacloud.nasa.gov/
  - https://lpdaac.usgs.gov/products/mod11a1v061/
* **Accessed:** September 2026

### 4. Planetary Targets (Moon & Mars)
* **Description:** Orbital data, elevation, and thermal mosaics for candidate planetary base sites.
* **Source:** NASA Mars Trek / PDS Geosciences Node / PDS ODE API / Lunar Orbiter
* **URLs:**
  - https://trek.nasa.gov/mars/
  - https://pds-geosciences.wustl.edu/
  - https://oderest.rsl.wustl.edu/
  - https://pds-imaging.jpl.nasa.gov/tools/atlas/documentation/
  - https://www.lpi.usra.edu/resources/lunar_orbiter/bin/srch_crd.shtml?-90%7C90%7C-180%7C180%7C0
* **Accessed:** September 2026
