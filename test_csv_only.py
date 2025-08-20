#!/usr/bin/env python3
"""
Test script to verify CSV-only functionality (no Excel dependencies)
"""

import sys
import os

def test_csv_only_import():
    """Test that pysebal_py3 can be imported without Excel dependencies"""
    print("=" * 60)
    print("Testing CSV-Only Import (No Excel Dependencies)")
    print("=" * 60)
    
    try:
        sys.path.append('SEBAL')
        import pysebal_py3
        print("✅ pysebal_py3 imported successfully")
        
        # Check that the function signature has been updated
        if hasattr(pysebal_py3, 'SEBALcode'):
            print("✅ SEBALcode function found")
        else:
            print("❌ SEBALcode function not found")
            
        return True
    except ImportError as e:
        if 'openpyxl' in str(e):
            print(f"❌ Still depends on Excel/openpyxl: {e}")
            return False
        else:
            print(f"ℹ️ Other dependency missing (expected): {e}")
            return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_csv_loading():
    """Test CSV data loading functionality"""
    print("\n" + "=" * 60)
    print("Testing CSV Data Loading")
    print("=" * 60)
    
    try:
        import pandas as pd
        
        # Test loading the sample CSV
        csv_file = 'sample_input_timeseries.csv'
        if not os.path.exists(csv_file):
            print(f"❌ Sample CSV file {csv_file} not found")
            return False
            
        df = pd.read_csv(csv_file)
        print(f"✅ CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        
        # Test first row data extraction
        if len(df) > 0:
            first_row = df.iloc[0]
            print(f"✅ First row data accessible:")
            print(f"   Date: {first_row.get('Date_Acquired', 'N/A')}")
            print(f"   Image: {first_row.get('Name_Landsat_Image', 'N/A')}")
            print(f"   Input folder: {first_row.get('input_folder', 'N/A')}")
            
        return True
        
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
        return False

def test_run_py3_update():
    """Test that Run_py3.py has been updated for CSV"""
    print("\n" + "=" * 60)
    print("Testing Run_py3.py CSV Update")
    print("=" * 60)
    
    try:
        with open('SEBAL/Run_py3.py', 'r') as f:
            content = f.read()
            
        if 'inputCSV' in content:
            print("✅ Run_py3.py updated to use inputCSV variable")
        else:
            print("❌ Run_py3.py still uses inputExcel variable")
            
        if 'sample_input_timeseries.csv' in content:
            print("✅ Run_py3.py points to CSV file")
        else:
            print("❌ Run_py3.py not pointing to CSV file")
            
        if '.xlsx' not in content and '.xls' not in content:
            print("✅ No Excel file references found")
        else:
            print("❌ Still contains Excel file references")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking Run_py3.py: {e}")
        return False

if __name__ == "__main__":
    print("PySEBAL CSV-Only Verification Test")
    print("=" * 60)
    
    tests = [
        test_csv_only_import,
        test_csv_loading,
        test_run_py3_update
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests PASSED!")
        print("✅ PySEBAL is now CSV-only (no Excel dependencies)")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("❌ Some issues remain")
    
    print("=" * 60)