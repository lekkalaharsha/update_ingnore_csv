import pandas as pd
#AUTHOT:LEKKALA HARSHA

def compare_and_update(file1_path, file2_path, output_file_path, new_column_name, ignore_list):
    """
    Compare the 'Metric' columns from two CSV files and add a user-defined column
    to the first file indicating if each 'Metric' is present in the second file,
    ignoring specified metrics.

    Args:
        file1_path (str): Path to the first CSV file (to be updated).
        file2_path (str): Path to the second CSV file (to compare against).
        output_file_path (str): Path where the updated CSV file will be saved.
        new_column_name (str): Name of the new column to be added to the first file.
        ignore_list (list): List of Metric values to ignore during comparison.
    """
    # Load the CSV files into DataFrames
    file1_df = pd.read_csv(file1_path)
    file2_df = pd.read_csv(file2_path)
    
    # Create a set of unique Metric values from file2_df for quick lookup
    file2_metric_set = set(file2_df['Metric'])
    
    # Add a new column with the specified name to file1_df to indicate presence in file2_df
    file1_df[new_column_name] = file1_df['Metric'].apply(
        lambda x: 'Yes' if x in file2_metric_set and x not in ignore_list else 'No'
    )
    
    # Save the updated DataFrame to a new CSV file
    file1_df.to_csv(output_file_path, index=False)
    print(f"Updated file saved to: {output_file_path}")

# Paths to the input CSV files
file1_path = 'path/to/your/Vehicle_data_collection_checklist.csv'
file2_path = 'path/to/your/Panel_Title_data.csv'

# Output path for the updated CSV file
output_file_path = 'path/to/your/Updated_Vehicle_Data_Collection_Checklist.csv'

# Prompt the user for the new column name
new_column_name = input("Enter the name for the new column to indicate matches: ")

# List of Metric values to ignore
ignore_list = [
    'bms_battery_health.count_battery_voltage',
    'bms_battery_health.count_battery_current',
    'bms_state_limits.count_chrg_status',
    'bms_state_limits.count_chrgr_highest_current',
    'bms_state_limits.count_chrgr_highest_voltage'
]

# Run the function to compare and update
compare_and_update(file1_path, file2_path, output_file_path, new_column_name, ignore_list)
