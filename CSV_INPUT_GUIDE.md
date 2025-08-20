# PySEBAL CSV Input for Timeseries ET Calculations

This document explains how to use the modified PySEBAL with CSV input files for timeseries evapotranspiration (ET) calculations from Landsat images and weather station data.

## Overview

The modified PySEBAL now supports CSV input files in addition to the original Excel format. This enables easier automation and processing of timeseries data for multiple Landsat images with corresponding weather data.

## Features

- **CSV Input Support**: Process multiple dates from a single CSV file
- **Timeseries Processing**: Automatic processing of January to August 2025 data (or any date range)
- **Weather Data Integration**: Each Landsat image paired with field weather data
- **Automated ET Calculation**: SEBAL model calculations for each time step
- **Batch Processing**: Process all dates in sequence or specify date ranges

## CSV File Structure

The input CSV file should contain one row per Landsat image/date with the following columns:

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| `Date_Acquired` | Date of Landsat image acquisition | 2025-01-15 |
| `Name_Landsat_Image` | Landsat image identifier | LC09_L1TP_173049_20250115_20250115_02_T1 |
| `input_folder` | Path to Landsat image files | /path/to/landsat/2025_01_15 |
| `output_folder` | Path where results will be saved | /path/to/output/2025_01_15 |
| `Image_Type` | Type of satellite image (1=Landsat) | 1 |
| `DEM_fileName` | Path to Digital Elevation Model file | /path/to/dem/dem.tif |

### Landsat Parameters

| Column | Description | Example |
|--------|-------------|---------|
| `Landsat_nr` | Landsat satellite number (8 or 9) | 9 |
| `Thermal_Bands` | Number of thermal bands | 2 |
| `tcoldmin` | Minimum percentile for cold pixels | 5 |
| `tcoldmax` | Maximum percentile for cold pixels | 10 |
| `ndvihot_low` | NDVI low percentile for hot pixels | 2 |
| `ndvihot_high` | NDVI high percentile for hot pixels | 8 |
| `ndvicold_low` | NDVI low percentile for cold pixels | 75 |
| `ndvicold_high` | NDVI high percentile for cold pixels | 95 |
| `Hot_Pixel_Constant` | Hot pixel calibration constant | 0 |
| `Cold_Pixel_Constant` | Cold pixel calibration constant | 0 |

### Weather Data (Field/Station Data)

| Column | Description | Units | Example |
|--------|-------------|--------|---------|
| `Temp_inst` | Instantaneous air temperature | °C | 18.5 |
| `Temp_24` | Daily average air temperature | °C | 16.2 |
| `RH_inst` | Instantaneous relative humidity | % | 65 |
| `RH_24` | Daily average relative humidity | % | 58 |
| `Wind_inst` | Instantaneous wind speed | m/s | 2.1 |
| `Wind_24` | Daily average wind speed | m/s | 2.8 |
| `zx` | Height of wind measurement | m | 10 |

### Radiation Parameters

| Column | Description | Units | Example |
|--------|-------------|--------|---------|
| `Method_Radiation_24` | Daily radiation method (1=Rs_24, 2=Transm_24) | - | 1 |
| `Method_Radiation_inst` | Instantaneous radiation method (1=Rs_inst, 2=Transm_inst) | - | 1 |
| `Rs_24` | Daily surface solar radiation | W/m² | 185 |
| `Rs_in_inst` | Instantaneous surface solar radiation | W/m² | 580 |
| `Transm_24` | Daily transmissivity (if Method_Radiation_24=2) | - | 0.75 |
| `Transm_inst` | Instantaneous transmissivity (if Method_Radiation_inst=2) | - | 0.80 |

### Soil Parameters (Optional)

| Column | Description | Units | Example |
|--------|-------------|--------|---------|
| `Theta_sat_top` | Saturated soil moisture content (topsoil) | m³/m³ | 0.45 |
| `Theta_sat_sub` | Saturated soil moisture content (subsoil) | m³/m³ | 0.42 |
| `Theta_res_top` | Residual soil moisture content (topsoil) | m³/m³ | 0.08 |
| `Theta_res_sub` | Residual soil moisture content (subsoil) | m³/m³ | 0.05 |
| `Field_Capacity` | Field capacity | m³/m³ | 0.35 |
| `Soil_moisture_wilting_point` | Wilting point | m³/m³ | 0.15 |
| `LUEmax` | Maximum light use efficiency | g/MJ | 2.5 |
| `h_obst` | Obstacle height | m | 0.1 |
| `depl_factor` | Depletion factor | - | 0.5 |

## Usage

### 1. Prepare Your Data

1. **Landsat Images**: Organize Landsat images in separate folders for each date
2. **Weather Data**: Collect field weather station data for each Landsat acquisition date
3. **DEM File**: Prepare a Digital Elevation Model covering your study area
4. **CSV File**: Create a CSV file with all input parameters

### 2. Create CSV Input File

Use the provided template `sample_input_timeseries.csv` and modify it with your data:

```bash
# Copy the sample file
cp sample_input_timeseries.csv my_input_data.csv

# Edit with your actual paths and data
# Update paths to your Landsat images, output folders, DEM file
# Update weather data with your field measurements
```

### 3. Run Timeseries Processing

```bash
# Process all rows in the CSV
python run_timeseries.py my_input_data.csv

# Process specific rows (e.g., rows 1-5)
python run_timeseries.py my_input_data.csv 1 5

# Process from a specific row to the end
python run_timeseries.py my_input_data.csv 3
```

### 4. Monitor Progress

The script will display progress for each processing run:

```
======================================================================
PySEBAL Timeseries ET Calculation with CSV Input
======================================================================
Input file: my_input_data.csv
✓ CSV validation passed. Found 8 rows to process.
Processing range: rows 1 to 8 (8 total runs)
======================================================================

------------------------------------------------------------
Processing run 1/8
Date: 2025-01-15
Image: LC09_L1TP_173049_20250115_20250115_02_T1
Output: /path/to/output/2025_01_15
------------------------------------------------------------
Starting SEBAL processing...
✓ Run 1 completed successfully
```

### 5. Results

For each processing run, SEBAL will generate:

- **ET Maps**: Actual, potential, and reference evapotranspiration
- **Energy Balance Components**: Net radiation, soil heat flux, sensible heat flux
- **Vegetation Parameters**: NDVI, SAVI, LAI, vegetation cover
- **Temperature Maps**: Surface temperature, corrected temperature
- **Other Outputs**: Albedo, biomass production, water productivity

Results are saved in the specified output folders with standardized naming conventions.

## Example CSV Format

See `sample_input_timeseries.csv` for a complete example with 8 months of data (January-August 2025).

## Troubleshooting

### Common Issues

1. **File Path Errors**: Ensure all paths in the CSV are correct and accessible
2. **Missing Landsat Files**: Verify that all required Landsat band files are present
3. **DEM File Issues**: Ensure DEM file covers the entire Landsat scene extent
4. **Memory Issues**: For large scenes, ensure sufficient RAM is available

### Error Messages

- `Error: Missing required columns in CSV`: Add the missing columns to your CSV
- `Error: CSV file not found`: Check the file path and name
- `Error loading CSV file`: Check CSV format and encoding

## Performance Tips

1. **Parallel Processing**: Process different date ranges on separate machines
2. **Storage**: Use fast SSD storage for input/output operations
3. **Memory**: Ensure adequate RAM (8GB+ recommended)
4. **Temporary Files**: Ensure sufficient disk space for temporary processing files

## Output Analysis

After processing, you can analyze the timeseries ET results:

1. **Load ET Maps**: Use GIS software to load the generated ET rasters
2. **Time Series Analysis**: Extract ET values for specific locations or regions
3. **Seasonal Patterns**: Analyze ET variations from January to August
4. **Water Balance**: Combine ET with precipitation data for water balance studies
5. **Irrigation Management**: Use ET data for irrigation scheduling and water management