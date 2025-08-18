# dss_parser.py
from pydss import HecDss
import pandas as pd
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_dss_data(dss_file_path: str, dss_path: str) -> list:
    """
    Reads time-series data from a DSS file for a specific path.

    Args:
        dss_file_path: The path to the DSS file.
        dss_path: The full path to the time-series data within the DSS file (e.g., '/PANCHGANGA/RAJARAM BRIDGE/FLOW/01JAN2021/1DAY/OBS/').

    Returns:
        A list of dictionaries with 'timestamp' and 'value' for each data point.
    """
    try:
        # Open the DSS file in a context manager to ensure it's closed properly
        with HecDss.open(dss_file_path) as dss_file:
            # Check if the DSS file is valid
            if not dss_file:
                raise ValueError(f"Invalid DSS file: {dss_file_path}")

            logging.info(f"Successfully opened DSS file: {dss_file_path}")

            # Get the data from the specified path
            ts = dss_file.read_ts(dss_path, validate=True)

            if ts is None:
                raise ValueError(f"No data found for path: {dss_path}")

            logging.info(f"Successfully read data for path: {dss_path}")

            # Convert the time-series data to a Pandas DataFrame
            # The 'ts.values' are a numpy array of values
            # The 'ts.times' are a list of datetime objects
            df = pd.DataFrame({
                'timestamp': ts.times,
                'value': ts.values
            })

            # Handle the case where the data might be empty
            if df.empty:
                raise ValueError("Extracted DataFrame is empty.")

            # Convert to a list of dictionaries for JSON serialization
            data_list = df.to_dict('records')
            
            logging.info("Data successfully converted to list of dictionaries.")
            return data_list

    except FileNotFoundError:
        logging.error(f"Error: DSS file not found at {dss_file_path}")
        return []
    except ValueError as ve:
        logging.error(f"Data extraction error: {ve}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []

if __name__ == '__main__':
    # This block is for testing the function directly
    # Make sure to replace this path with the actual path to your .dss file
    test_dss_file_path = 'path/to/your/Rajaram_Bridge_DailyDischarge_2021_July.dss'
    
    # This path must match the exact data path in your DSS file
    test_dss_path = '/PANCHGANGA/RAJARAM BRIDGE/FLOW/01JUL2021/1DAY/OBS/'

    print(f"Testing the DSS parser with file: {test_dss_file_path} and path: {test_dss_path}")
    
    extracted_data = read_dss_data(test_dss_file_path, test_dss_path)

    if extracted_data:
        print(f"Successfully extracted {len(extracted_data)} data points.")
        # Print the first 5 data points for verification
        print("First 5 data points:")
        for item in extracted_data[:5]:
            print(item)
    else:
        print("Failed to extract data.")