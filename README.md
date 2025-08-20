# PySEBAL

PySEBAL implements Surface Energy Balance Model for Land (SEBAL) in python to estimate spatially explicit Actual EvapoTranspiration maps from remotely sensed data. In addition the library also computes various outputs like Above Ground Biomass Production (AGBP) and Biomass Water Productivity AGBP is computed using fAPAR and LUE factors as inputs. The library is extensively tested on Landsat 7 and 8 data, however it should also support MODIS and PROBA-V/VIIRS. Th library supports python 3 and run in both Windows and Linux operating systems.

## NEW: CSV Input for Timeseries Processing

PySEBAL now supports **CSV input files** for automated timeseries evapotranspiration calculations! This feature enables:

- **Timeseries ET Analysis**: Process multiple Landsat images (e.g., January-August 2025) with corresponding weather data
- **Field Weather Integration**: Each Landsat image paired with field weather station data  
- **Automated Processing**: Batch processing of multiple dates from a single CSV file
- **Easy Data Management**: Simple CSV format instead of complex Excel sheets

### Quick Start with CSV Input

1. **Prepare your CSV file** with Landsat images and weather data:
```bash
# Use the provided template
cp sample_input_timeseries.csv my_data.csv
# Edit with your actual data paths and weather measurements
```

2. **Run timeseries processing**:
```bash
# Process all dates
python run_timeseries.py my_data.csv

# Process specific date range  
python run_timeseries.py my_data.csv 1 5
```

3. **Get ET maps for each date** with automated SEBAL calculations

### Documentation

- [📋 CSV Input Guide](CSV_INPUT_GUIDE.md) - Complete guide for CSV input format
- [🚀 Example Workflow](EXAMPLE_WORKFLOW.md) - Step-by-step example for Jan-Aug 2025 timeseries
- [📊 Sample CSV File](sample_input_timeseries.csv) - Template with 8 months of data

## Original Documentation
Documentation on how to install, setup and run PySEBAL is provided here: https://pysebal.readthedocs.io/

## Contact
For questions, please contact the wateraccounting group at IHE Delft.
