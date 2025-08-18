# dss_parser.py
from hecdss import HecDss
import pandas as pd
import logging
import matplotlib.pyplot as plt

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_dss_data(dss_file_path: str, dss_path: str) -> list:
    """
    Reads time-series data from a DSS file for a specific path.

    Args:
        dss_file_path: The path to the DSS file.
        dss_path: The full path to the time-series data within the DSS file.

    Returns:
        A list of dictionaries with 'timestamp' and 'value' for each data point.
    """
    try:
        with HecDss(dss_file_path) as dss_file:
            ts = dss_file.get(dss_path)

            if ts is None:
                raise ValueError(f"No data found for path: {dss_path}")

            logging.info(f"Successfully read data for path: {dss_path}")

            # Convert to DataFrame
            df = pd.DataFrame({
                'timestamp': ts.times,
                'value': ts.values
            })

            if df.empty:
                raise ValueError("Extracted DataFrame is empty.")

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


# Test runner
if __name__ == "__main__":
    test_dss_file_path = "Rajaram_Bridge_DailyDischarge_2021_July.dss"
    test_dss_path = "/Panchganga/Rajaram Bridge/FLOW/01Jan2021/1Day/Observed Discharge/"

    print(f"Testing DSS parser with file: {test_dss_file_path} and path: {test_dss_path}")

    extracted_data = read_dss_data(test_dss_file_path, test_dss_path)

    if extracted_data:
        print(f"✅ Successfully extracted {len(extracted_data)} data points.")
        print("First 5 rows:")
        for row in extracted_data[:5]:
            print(row)

        # Quick plot
        df = pd.DataFrame(extracted_data)
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["value"], marker="o")
        plt.title("Observed Discharge at Rajaram Bridge")
        plt.xlabel("Date")
        plt.ylabel("Discharge (cms)")
        plt.grid(True)
        plt.show()
    else:
        print("❌ No data extracted.")
