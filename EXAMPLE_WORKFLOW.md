# PySEBAL Timeseries ET Calculation Example

This example demonstrates how to use the CSV input system for processing multiple Landsat images with weather data to calculate timeseries evapotranspiration (ET).

## Scenario

You have:
- Landsat 9 images for 8 dates from January to August 2025
- Weather station data for each date (temperature, humidity, wind speed, radiation)
- A Digital Elevation Model (DEM) for your study area
- Need to calculate ET for each date to create a timeseries

## Step 1: Prepare Your Data Structure

```
your_project/
├── landsat_images/
│   ├── 2025_01_15/
│   │   ├── LC09_L1TP_173049_20250115_20250115_02_T1_B1.TIF
│   │   ├── LC09_L1TP_173049_20250115_20250115_02_T1_B2.TIF
│   │   ├── ... (all bands)
│   │   └── LC09_L1TP_173049_20250115_20250115_02_T1_MTL.txt
│   ├── 2025_02_10/
│   │   └── ... (similar structure)
│   └── ... (more dates)
├── dem/
│   └── study_area_dem.tif
├── weather_data/
│   └── weather_station_data.csv
└── outputs/
    ├── 2025_01_15/
    ├── 2025_02_10/
    └── ... (results for each date)
```

## Step 2: Create CSV Input File

Create `et_timeseries_input.csv` with your actual data:

```csv
Date_Acquired,Name_Landsat_Image,input_folder,output_folder,Image_Type,DEM_fileName,Landsat_nr,Thermal_Bands,Temp_inst,Temp_24,RH_inst,RH_24,Wind_inst,Wind_24,zx,Method_Radiation_24,Method_Radiation_inst,Rs_24,Rs_in_inst,Transm_24,Transm_inst,tcoldmin,tcoldmax,ndvihot_low,ndvihot_high,ndvicold_low,ndvicold_high,Hot_Pixel_Constant,Cold_Pixel_Constant,Theta_sat_top,Theta_sat_sub,Theta_res_top,Theta_res_sub,Field_Capacity,Soil_moisture_wilting_point,LUEmax,h_obst,depl_factor
2025-01-15,LC09_L1TP_173049_20250115_20250115_02_T1,/your_project/landsat_images/2025_01_15,/your_project/outputs/2025_01_15,1,/your_project/dem/study_area_dem.tif,9,2,18.5,16.2,65,58,2.1,2.8,10,1,1,185,580,0.75,0.80,5,10,2,8,75,95,0,0,0.45,0.42,0.08,0.05,0.35,0.15,2.5,0.1,0.5
2025-02-10,LC09_L1TP_173049_20250210_20250210_02_T1,/your_project/landsat_images/2025_02_10,/your_project/outputs/2025_02_10,1,/your_project/dem/study_area_dem.tif,9,2,21.3,19.8,62,55,2.3,3.1,10,1,1,195,620,0.75,0.80,5,10,2,8,75,95,0,0,0.45,0.42,0.08,0.05,0.35,0.15,2.5,0.1,0.5
... (continue for all dates)
```

## Step 3: Run Timeseries Processing

### Process all dates:
```bash
python run_timeseries.py et_timeseries_input.csv
```

### Process specific date range:
```bash
# Process only January to March (rows 1-3)
python run_timeseries.py et_timeseries_input.csv 1 3

# Process from May onwards (row 5 to end)
python run_timeseries.py et_timeseries_input.csv 5
```

## Step 4: Monitor Progress

The script will show progress like this:

```
======================================================================
PySEBAL Timeseries ET Calculation with CSV Input
======================================================================
Input file: et_timeseries_input.csv
✓ CSV validation passed. Found 8 rows to process.
Processing range: rows 1 to 8 (8 total runs)
======================================================================

------------------------------------------------------------
Processing run 1/8
Date: 2025-01-15
Image: LC09_L1TP_173049_20250115_20250115_02_T1
Output: /your_project/outputs/2025_01_15
------------------------------------------------------------
Starting SEBAL processing...
[SEBAL processing details...]
✓ Run 1 completed successfully

------------------------------------------------------------
Processing run 2/8
Date: 2025-02-10
[...]
```

## Step 5: Results

After processing, each output folder will contain:

```
outputs/2025_01_15/
├── Output_evapotranspiration/
│   ├── L9_ETact_24_30m_2025_01_15_015.tif        # Daily actual ET
│   ├── L9_ETpot_24_30m_2025_01_15_015.tif        # Daily potential ET
│   ├── L9_ETref_24_30m_2025_01_15_015.tif        # Daily reference ET
│   └── ... (other ET components)
├── Output_energy_balance/
│   ├── L9_Rn_24_30m_2025_01_15_015.tif           # Net radiation
│   ├── L9_G_30m_2025_01_15_015.tif               # Soil heat flux
│   └── ... (other energy balance components)
├── Output_vegetation/
│   ├── L9_NDVI_30m_2025_01_15_015.tif            # NDVI
│   ├── L9_LAI_30m_2025_01_15_015.tif             # Leaf Area Index
│   └── ... (other vegetation parameters)
└── ... (other output folders)
```

## Step 6: Timeseries Analysis

After all dates are processed, you can:

1. **Load ET maps in GIS software** (QGIS, ArcGIS, etc.)
2. **Extract timeseries** for specific locations or regions
3. **Analyze seasonal patterns** from January to August
4. **Calculate water balance** components
5. **Generate irrigation schedules** based on ET data

### Example Python analysis:
```python
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load ET maps for all dates
dates = ['2025-01-15', '2025-02-10', '2025-03-12', '2025-04-08', 
         '2025-05-14', '2025-06-15', '2025-07-17', '2025-08-18']

et_values = []
for date in dates:
    et_file = f'/your_project/outputs/{date}/Output_evapotranspiration/L9_ETact_24_30m_{date.replace("-", "_")}_*.tif'
    with rasterio.open(et_file) as src:
        et_data = src.read(1)
        # Calculate mean ET for the area
        mean_et = np.nanmean(et_data)
        et_values.append(mean_et)

# Plot timeseries
plt.figure(figsize=(12, 6))
plt.plot(dates, et_values, 'o-', linewidth=2, markersize=8)
plt.title('Timeseries Evapotranspiration (Jan-Aug 2025)')
plt.xlabel('Date')
plt.ylabel('ET (mm/day)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## Weather Data Integration

Each row in the CSV corresponds to the weather conditions during Landsat image acquisition:

- **Temperature**: Instantaneous and daily average air temperature
- **Humidity**: Instantaneous and daily average relative humidity  
- **Wind Speed**: Instantaneous and daily average wind speed
- **Solar Radiation**: Incoming solar radiation or atmospheric transmissivity

This ensures that ET calculations account for the actual meteorological conditions during each satellite overpass.

## Tips for Success

1. **Data Quality**: Ensure weather data is collected close in time to Landsat acquisition
2. **Spatial Consistency**: Weather station should be representative of the study area
3. **Cloud Screening**: Use cloud-free Landsat images for best results
4. **Validation**: Compare results with ground-based ET measurements if available
5. **Seasonal Analysis**: Look for patterns related to crop growth stages or seasonal changes

## Troubleshooting

### Common Issues:

1. **Path Errors**: Double-check all file paths in the CSV
2. **Missing Bands**: Ensure all Landsat bands are present and correctly named
3. **DEM Extent**: DEM should cover the entire Landsat scene
4. **Memory**: Large scenes may require significant RAM (8GB+ recommended)

### Error Solutions:

- **"File not found"**: Verify file paths and permissions
- **"Invalid projection"**: Ensure DEM and Landsat images have compatible projections
- **"Out of memory"**: Process smaller areas or use a machine with more RAM

This workflow enables systematic processing of multiple Landsat images to create comprehensive ET timeseries for agricultural monitoring, water management, and climate studies.