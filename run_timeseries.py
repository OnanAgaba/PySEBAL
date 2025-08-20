# -*- coding: utf-8 -*-
"""
PySEBAL CSV Runner for Timeseries ET Calculations

This script processes multiple Landsat images and weather data from a CSV file
to calculate timeseries Evapotranspiration using the SEBAL model.

@author: Modified for CSV timeseries support
"""

import os
import sys
import traceback
import pandas as pd

# Add the SEBAL directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sebal_dir = os.path.join(current_dir, 'SEBAL')
if sebal_dir not in sys.path:
    sys.path.insert(0, sebal_dir)

# Import the modified SEBAL code
from SEBAL import pysebal_py3

def validate_csv_input(csv_file):
    """
    Validate CSV input file and check required columns
    """
    required_columns = [
        'input_folder', 'output_folder', 'Image_Type', 'DEM_fileName',
        'Name_Landsat_Image', 'Date_Acquired'
    ]
    
    try:
        df = pd.read_csv(csv_file)
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing required columns in CSV: {missing_columns}")
            return False, None
        
        print(f"✓ CSV validation passed. Found {len(df)} rows to process.")
        return True, df
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False, None

def run_timeseries_processing(csv_file, start_row=1, end_row=None):
    """
    Process timeseries SEBAL calculations from CSV input
    
    Parameters:
    csv_file (str): Path to CSV input file
    start_row (int): Starting row number (1-based)
    end_row (int): Ending row number (1-based, None for all rows)
    """
    
    print('=' * 70)
    print('PySEBAL Timeseries ET Calculation with CSV Input')
    print('=' * 70)
    print(f'Input file: {csv_file}')
    
    # Validate CSV input
    is_valid, df = validate_csv_input(csv_file)
    if not is_valid:
        return False
    
    # Determine processing range
    total_rows = len(df)
    if end_row is None:
        end_row = total_rows
    else:
        end_row = min(end_row, total_rows)
    
    start_idx = start_row - 1  # Convert to 0-based index
    end_idx = end_row
    
    print(f'Processing range: rows {start_row} to {end_row} ({end_idx - start_idx} total runs)')
    print('=' * 70)
    
    # Track results
    successful_runs = 0
    failed_runs = 0
    results = []
    
    # Process each row
    for i in range(start_idx, end_idx):
        row_number = i + 1  # Convert back to 1-based for display
        excel_row = i + 2   # Excel-style row numbering (row 2 = first data row)
        
        try:
            # Get run information
            row_data = df.iloc[i]
            date_acquired = row_data.get('Date_Acquired', 'Unknown')
            image_name = row_data.get('Name_Landsat_Image', 'Unknown')
            output_folder = row_data.get('output_folder', 'Unknown')
            
            print(f'\n{"-" * 60}')
            print(f'Processing run {row_number}/{total_rows}')
            print(f'Date: {date_acquired}')
            print(f'Image: {image_name}')
            print(f'Output: {output_folder}')
            print(f'{"-" * 60}')
            
            # Run SEBAL processing
            print('Starting SEBAL processing...')
            result = pysebal_py3.SEBALcode(excel_row, csv_file)
            
            print(f'✓ Run {row_number} completed successfully')
            successful_runs += 1
            
            results.append({
                'run_number': row_number,
                'date': date_acquired,
                'image': image_name,
                'output_folder': output_folder,
                'status': 'Success',
                'error': None
            })
            
        except Exception as e:
            print(f'✗ Run {row_number} failed with error:')
            print(f'Error: {str(e)}')
            # Print traceback for debugging
            traceback.print_exc()
            failed_runs += 1
            
            results.append({
                'run_number': row_number,
                'date': date_acquired if 'date_acquired' in locals() else 'Unknown',
                'image': image_name if 'image_name' in locals() else 'Unknown', 
                'output_folder': output_folder if 'output_folder' in locals() else 'Unknown',
                'status': 'Failed',
                'error': str(e)
            })
    
    # Print summary
    print(f'\n{"=" * 70}')
    print('TIMESERIES PROCESSING COMPLETED')
    print(f'{"=" * 70}')
    print(f'Total runs processed: {successful_runs + failed_runs}')
    print(f'Successful runs: {successful_runs}')
    print(f'Failed runs: {failed_runs}')
    print(f'Success rate: {(successful_runs/(successful_runs + failed_runs)*100):.1f}%')
    
    # Print detailed results
    print(f'\nDetailed Results:')
    print('-' * 70)
    for result in results:
        status_symbol = '✓' if result['status'] == 'Success' else '✗'
        print(f"{status_symbol} Run {result['run_number']}: {result['date']} - {result['image']}")
        if result['error']:
            print(f"    Error: {result['error']}")
    
    print(f'{"=" * 70}')
    
    return successful_runs > 0

def main():
    """Main function for command line execution"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_timeseries.py <csv_input_file>")
        print("  python run_timeseries.py <csv_input_file> <start_row> [end_row]")
        print("")
        print("Examples:")
        print("  python run_timeseries.py sample_input_timeseries.csv")
        print("  python run_timeseries.py sample_input_timeseries.csv 1 5")
        print("")
        print("CSV file should contain columns for:")
        print("  - input_folder: Path to Landsat images")
        print("  - output_folder: Where to save results")
        print("  - Image_Type: 1 for Landsat")
        print("  - DEM_fileName: Path to DEM file")
        print("  - Name_Landsat_Image: Landsat image name")
        print("  - Date_Acquired: Date of image acquisition")
        print("  - Weather data: Temp_inst, Temp_24, RH_inst, RH_24, Wind_inst, Wind_24, etc.")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    # Parse optional arguments
    start_row = 1
    end_row = None
    
    if len(sys.argv) > 2:
        try:
            start_row = int(sys.argv[2])
        except ValueError:
            print("Error: start_row must be an integer")
            sys.exit(1)
    
    if len(sys.argv) > 3:
        try:
            end_row = int(sys.argv[3])
        except ValueError:
            print("Error: end_row must be an integer")
            sys.exit(1)
    
    # Run processing
    success = run_timeseries_processing(csv_file, start_row, end_row)
    
    if success:
        print("\nTimeseries processing completed successfully!")
        sys.exit(0)
    else:
        print("\nTimeseries processing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()