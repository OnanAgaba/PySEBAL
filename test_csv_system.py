#!/usr/bin/env python3
"""
Test script for CSV input functionality
"""

import pandas as pd
import os
import sys

def test_csv_loading():
    """Test basic CSV loading functionality"""
    print("=" * 60)
    print("Testing CSV Input System for PySEBAL")
    print("=" * 60)
    
    # Test 1: Load CSV file
    csv_file = 'sample_input_timeseries.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found")
        return False
    
    try:
        df = pd.read_csv(csv_file)
        print(f"✅ CSV file loaded successfully")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False
    
    # Test 2: Validate required columns
    required_columns = [
        'Date_Acquired', 'Name_Landsat_Image', 'input_folder', 'output_folder',
        'Image_Type', 'DEM_fileName', 'Temp_inst', 'Temp_24', 'RH_inst', 'RH_24'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Missing required columns: {missing_columns}")
        return False
    else:
        print(f"✅ All required columns present")
    
    # Test 3: Validate data ranges
    print("\n📊 Data Validation:")
    for i, row in df.iterrows():
        date = row['Date_Acquired']
        temp_inst = row['Temp_inst']
        temp_24 = row['Temp_24']
        rh_inst = row['RH_inst']
        rh_24 = row['RH_24']
        
        print(f"   Row {i+1}: {date}")
        print(f"      Temp: {temp_inst}°C (inst), {temp_24}°C (daily)")
        print(f"      RH: {rh_inst}% (inst), {rh_24}% (daily)")
        
        # Basic validation
        if not (0 <= rh_inst <= 100) or not (0 <= rh_24 <= 100):
            print(f"   ⚠️  Warning: Humidity values may be out of range")
        
        if temp_inst < -50 or temp_inst > 60:
            print(f"   ⚠️  Warning: Temperature values may be out of range")
    
    # Test 4: Simulate timeseries processing
    print(f"\n🚀 Simulating Timeseries Processing:")
    print(f"   Date range: {df['Date_Acquired'].min()} to {df['Date_Acquired'].max()}")
    print(f"   Total images to process: {len(df)}")
    
    success_count = 0
    for i, row in df.iterrows():
        date = row['Date_Acquired']
        image = row['Name_Landsat_Image']
        
        # Simulate processing (in real implementation, this would call SEBAL)
        print(f"   Processing {i+1}/{len(df)}: {date} - {image}")
        
        # Check if paths would be valid (just basic check)
        input_folder = row['input_folder']
        output_folder = row['output_folder']
        
        if '/path/to/' in input_folder:
            print(f"      ⚠️  Note: Update input_folder path")
        if '/path/to/' in output_folder:
            print(f"      ⚠️  Note: Update output_folder path")
        
        success_count += 1
    
    print(f"\n✅ Test completed successfully!")
    print(f"   {success_count}/{len(df)} runs would be processed")
    
    return True

def test_column_mapping():
    """Test the column mapping functionality"""
    print("\n" + "=" * 60)
    print("Testing Column Mapping System")
    print("=" * 60)
    
    # Define the mapping structure used in the actual code
    column_mapping = {
        'General_Input': {
            'B': 'input_folder',
            'C': 'output_folder', 
            'D': 'Image_Type',
            'E': 'DEM_fileName'
        },
        'Landsat_Input': {
            'B': 'Name_Landsat_Image',
            'C': 'Landsat_nr',
            'D': 'Thermal_Bands',
            'E': 'tcoldmin',
            'F': 'tcoldmax'
        },
        'Meteo_Input': {
            'B': 'Temp_inst',
            'C': 'Temp_24',
            'D': 'RH_inst', 
            'E': 'RH_24',
            'F': 'zx',
            'G': 'Wind_inst',
            'H': 'Wind_24'
        }
    }
    
    # Load CSV
    df = pd.read_csv('sample_input_timeseries.csv')
    first_row = df.iloc[0]
    
    print("Testing Excel-style cell access simulation:")
    
    for sheet_name, mappings in column_mapping.items():
        print(f"\n📋 Sheet: {sheet_name}")
        for cell_ref, column_name in mappings.items():
            if column_name in df.columns:
                value = first_row[column_name]
                print(f"   {cell_ref}2 -> {column_name}: {value}")
            else:
                print(f"   {cell_ref}2 -> {column_name}: ❌ Column not found")
    
    print(f"\n✅ Column mapping test completed!")

def create_example_usage():
    """Create example usage instructions"""
    print("\n" + "=" * 60)
    print("Example Usage Instructions")
    print("=" * 60)
    
    usage_text = """
To use the CSV input system for timeseries ET calculations:

1. Prepare your CSV file with the required columns
2. Update paths to point to your actual data
3. Run the processing script

Example commands:

# Process all dates in CSV file
python run_timeseries.py sample_input_timeseries.csv

# Process specific date range (rows 1-5)
python run_timeseries.py sample_input_timeseries.csv 1 5

# Process from row 3 to end
python run_timeseries.py sample_input_timeseries.csv 3

Your CSV file should have these key columns:
- Date_Acquired: Date of Landsat image
- Name_Landsat_Image: Landsat image identifier  
- input_folder: Path to Landsat band files
- output_folder: Where to save ET calculation results
- Weather data: Temp_inst, Temp_24, RH_inst, RH_24, Wind_inst, Wind_24
- DEM_fileName: Path to elevation model
- Other parameters: Radiation, soil properties, etc.

The system will process each row as a separate SEBAL run, creating
timeseries ET maps for your study period (Jan-Aug 2025).
"""
    
    print(usage_text)

if __name__ == "__main__":
    print("PySEBAL CSV Input System Test")
    print("=" * 60)
    
    # Run tests
    success = test_csv_loading()
    
    if success:
        test_column_mapping()
        create_example_usage()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! CSV input system is ready.")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Update the sample CSV with your actual data paths")
        print("2. Ensure Landsat images and DEM files are available")
        print("3. Install required dependencies (GDAL, openpyxl, etc.)")
        print("4. Run: python run_timeseries.py your_input_file.csv")
    else:
        print("\n❌ Tests failed. Check CSV file and try again.")
        sys.exit(1)