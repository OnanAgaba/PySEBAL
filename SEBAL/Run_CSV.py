# -*- coding: utf-8 -*-
"""
Modified PySEBAL main runner to support CSV input for timeseries processing

@author: Modified for CSV timeseries support
"""

import pandas as pd
import os
import sys
import traceback
from SEBAL import pysebal_py3

class CSVInputHandler:
    """Class to handle CSV input for PySEBAL"""
    
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = None
        self.load_csv()
    
    def load_csv(self):
        """Load CSV file into pandas DataFrame"""
        try:
            self.data = pd.read_csv(self.csv_file_path)
            print(f"Successfully loaded CSV with {len(self.data)} rows")
            return True
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return False
    
    def get_row_count(self):
        """Get number of rows in CSV"""
        return len(self.data) if self.data is not None else 0
    
    def get_value(self, sheet_name, cell_ref, row_index):
        """
        Get value from CSV data, mimicking Excel cell access
        
        Parameters:
        sheet_name (str): Sheet name (not used for CSV, kept for compatibility)
        cell_ref (str): Cell reference like 'B2', 'C3', etc.
        row_index (int): Row index (1-based to match Excel convention)
        
        Returns:
        Value from CSV or None if not found
        """
        if self.data is None:
            return None
        
        # Convert Excel-style cell reference to pandas column access
        col_letter = cell_ref[0]  # Get first letter (column)
        
        # Map common Excel columns to CSV column names
        col_mapping = {
            'A': 'Date_Acquired',
            'B': 'input_folder', 
            'C': 'output_folder',
            'D': 'Image_Type',
            'E': 'DEM_fileName',
            'F': 'Name_Landsat_Image',
            'G': 'Landsat_nr',
            'H': 'Thermal_Bands',
            'I': 'tcoldmin',
            'J': 'tcoldmax',
            'K': 'ndvihot_low',
            'L': 'ndvihot_high',
            'M': 'ndvicold_low',
            'N': 'ndvicold_high',
            'O': 'Hot_Pixel_Constant',
            'P': 'Cold_Pixel_Constant'
        }
        
        # For Meteo_Input sheet mapping
        if sheet_name == 'Meteo_Input':
            meteo_mapping = {
                'A': 'Date_Acquired',
                'B': 'Temp_inst',
                'C': 'Temp_24', 
                'D': 'RH_inst',
                'E': 'RH_24',
                'F': 'zx',
                'G': 'Wind_inst',
                'H': 'Wind_24',
                'I': 'Method_Radiation_24',
                'J': 'Rs_24',
                'K': 'Transm_24',
                'L': 'Method_Radiation_inst',
                'M': 'Rs_in_inst',
                'N': 'Transm_inst'
            }
            col_mapping.update(meteo_mapping)
        
        # Get column name from mapping
        if col_letter in col_mapping:
            col_name = col_mapping[col_letter]
        else:
            # Fallback to numeric column access
            col_index = ord(col_letter.upper()) - ord('A')
            if col_index < len(self.data.columns):
                col_name = self.data.columns[col_index]
            else:
                return None
        
        # Get value from specified row (convert to 0-based index)
        try:
            if col_name in self.data.columns:
                row_idx = row_index - 2  # Convert Excel row to pandas index (row 2 = index 0)
                if 0 <= row_idx < len(self.data):
                    value = self.data.iloc[row_idx][col_name]
                    return value if pd.notna(value) else None
        except:
            pass
        
        return None

# Create a mock workbook class to replace openpyxl for CSV inputs
class MockWorkbook:
    """Mock workbook class to replace openpyxl workbook for CSV inputs"""
    
    def __init__(self, csv_handler):
        self.csv_handler = csv_handler
        self.sheets = {
            'General_Input': MockWorksheet('General_Input', csv_handler),
            'Meteo_Input': MockWorksheet('Meteo_Input', csv_handler),
            'Landsat_Input': MockWorksheet('Landsat_Input', csv_handler),
            'Soil_Input': MockWorksheet('Soil_Input', csv_handler)
        }
    
    def __getitem__(self, sheet_name):
        return self.sheets.get(sheet_name, MockWorksheet(sheet_name, self.csv_handler))

class MockWorksheet:
    """Mock worksheet class to replace openpyxl worksheet for CSV inputs"""
    
    def __init__(self, sheet_name, csv_handler):
        self.sheet_name = sheet_name
        self.csv_handler = csv_handler
    
    def __getitem__(self, cell_ref):
        return MockCell(self.sheet_name, cell_ref, self.csv_handler)

class MockCell:
    """Mock cell class to replace openpyxl cell for CSV inputs"""
    
    def __init__(self, sheet_name, cell_ref, csv_handler):
        self.sheet_name = sheet_name
        self.cell_ref = cell_ref
        self.csv_handler = csv_handler
        self._value = None
        self.row_index = 2  # Default to row 2 (first data row)
    
    def set_row_index(self, row_index):
        """Set the row index for this cell reference"""
        self.row_index = row_index
    
    @property
    def value(self):
        """Get the cell value from CSV data"""
        if self._value is None:
            self._value = self.csv_handler.get_value(self.sheet_name, self.cell_ref, self.row_index)
        return self._value

def SEBALcode_CSV_wrapper(row_number, csv_file_path):
    """
    Wrapper function to run SEBAL with CSV input
    
    Parameters:
    row_number (int): Row number in CSV to process (1-based)
    csv_file_path (str): Path to CSV input file
    """
    
    # Create CSV handler
    csv_handler = CSVInputHandler(csv_file_path)
    
    if csv_handler.data is None:
        print("Error: Could not load CSV file")
        return False
    
    # Create mock workbook
    mock_wb = MockWorkbook(csv_handler)
    
    # Temporarily replace the load_workbook function in pysebal_py3
    original_load_workbook = None
    if hasattr(pysebal_py3, 'load_workbook'):
        original_load_workbook = pysebal_py3.load_workbook
    
    def mock_load_workbook(filename):
        """Mock load_workbook function that returns our CSV-based workbook"""
        return mock_wb
    
    # Replace the load_workbook function
    pysebal_py3.load_workbook = mock_load_workbook
    
    # Update cell references to use the correct row
    for sheet_name, sheet in mock_wb.sheets.items():
        # This is a bit hacky, but we need to update the row index for all cell accesses
        sheet.row_index = row_number + 1  # Convert to Excel-style row numbering
    
    try:
        # Call the original SEBAL function with our mock Excel input
        result = pysebal_py3.SEBALcode(row_number + 1, csv_file_path)  # +1 for Excel-style numbering
        return result
    finally:
        # Restore original load_workbook function
        if original_load_workbook:
            pysebal_py3.load_workbook = original_load_workbook

def run_timeseries_CSV(csv_file_path, start_row=1, end_row=None):
    """
    Run PySEBAL for multiple rows in CSV file (timeseries processing)
    
    Parameters:
    csv_file_path (str): Path to CSV input file
    start_row (int): Starting row number (1-based, default=1)
    end_row (int): Ending row number (1-based, default=all rows)
    """
    
    print('=========================================================')
    print('PySEBAL Timeseries Processing with CSV Input')
    print('=========================================================')
    
    # Load CSV to determine number of rows
    csv_handler = CSVInputHandler(csv_file_path)
    
    if csv_handler.data is None:
        print("Error: Could not load CSV file")
        return
    
    total_rows = csv_handler.get_row_count()
    
    if end_row is None:
        end_row = total_rows
    
    # Validate row range
    end_row = min(end_row, total_rows)
    
    print(f"Processing rows {start_row} to {end_row} ({end_row - start_row + 1} total runs)")
    
    successful_runs = 0
    failed_runs = 0
    
    # Process each row
    for row_num in range(start_row - 1, end_row):  # Convert to 0-based for processing
        try:
            print(f'\n{"="*60}')
            print(f'Starting processing for row {row_num + 1}/{total_rows}')
            
            # Get date and image info for logging
            date_acquired = csv_handler.get_value('General_Input', 'A', row_num + 2)
            image_name = csv_handler.get_value('General_Input', 'F', row_num + 2)
            
            print(f'Date: {date_acquired}')
            print(f'Image: {image_name}')
            print(f'{"="*60}')
            
            # Run SEBAL for this row
            SEBALcode_CSV_wrapper(row_num, csv_file_path)
            
            print(f'✓ Row {row_num + 1} completed successfully')
            successful_runs += 1
            
        except Exception as e:
            print(f'✗ Row {row_num + 1} failed with error:')
            print(f'Error: {e}')
            traceback.print_exc()
            failed_runs += 1
    
    print(f'\n{"="*60}')
    print('Timeseries processing completed')
    print(f'Successful runs: {successful_runs}')
    print(f'Failed runs: {failed_runs}')
    print(f'Total runs: {successful_runs + failed_runs}')
    print(f'{"="*60}')

if __name__ == "__main__":
    """Main execution for CSV-based PySEBAL"""
    
    if len(sys.argv) < 2:
        print("Usage: python Run_CSV.py <csv_input_file> [start_row] [end_row]")
        print("Example: python Run_CSV.py sample_input_timeseries.csv")
        print("Example: python Run_CSV.py sample_input_timeseries.csv 1 5")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    # Parse optional row range arguments
    start_row = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end_row = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    print(f"Processing CSV file: {csv_file}")
    
    # Run timeseries processing
    run_timeseries_CSV(csv_file, start_row, end_row)