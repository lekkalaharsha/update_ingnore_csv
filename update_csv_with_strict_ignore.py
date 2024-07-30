import pandas as pd

def compare_and_update(file1_path, file2_path, output_file_path, new_column_name, ignore_list):
    """
    Compare the 'Metric' columns from two CSV files and add a user-defined column
    to the first file indicating if each 'Metric' is present in the second file,
    ensuring ignored metrics are always marked 'No' and handling specific metric logic.

    Args:
        file1_path (str): Path to the first CSV file (to be updated).
        file2_path (str): Path to the second CSV file (to compare against).
        output_file_path (str): Path where the updated CSV file will be saved.
        new_column_name (str): Name of the new column to be added to the first file.
        ignore_list (list): List of Metric values to always mark as 'No'.
    """
    # Load the CSV files into DataFrames
    file1_df = pd.read_csv(file1_path)
    file2_df = pd.read_csv(file2_path)
    
    # Create a set of unique Metric values from file2_df for quick lookup
    file2_metric_set = set(file2_df['Metric'])
    
    # Define specific metrics to check
    specific_metrics = {
        'controller_motor_status_1_REAR.count_motorcontroller_1_controller_temp': 'controller_motor_status_1_REAR',
        'controller_motor_status_2_FRONT.count_motorcontroller_2_controller_temp': 'controller_motor_status_2_FRONT'
    }
    
    # Initialize the new column
    file1_df[new_column_name] = 'No'

    # Iterate through each metric in the first file
    for idx, row in file1_df.iterrows():
        metric = row['Metric']

        # Check if the metric should always be 'No'
        if metric in ignore_list:
            file1_df.at[idx, new_column_name] = 'No'
            continue

        # Check if the metric is present in the second file
        if metric in file2_metric_set:
            file1_df.at[idx, new_column_name] = 'Yes'
        
        # Handle specific logic for controller status
        for key_metric, related_metric in specific_metrics.items():
            if metric == related_metric and key_metric in file2_metric_set:
                file1_df.at[idx, new_column_name] = 'Yes'

    # Save the updated DataFrame to a new CSV file
    file1_df.to_csv(output_file_path, index=False)
    print(f"Updated file saved to: {output_file_path}")

# Paths to the input CSV files
file1_path = 'Updated_Vehicle_Data.csv'
file2_path = 'Panel Title-data-2024-07-29 18_14_07.csv'

# Output path for the updated CSV file
output_file_path = 'Updated_Vehicle_Data_3.csv'

# Prompt the user for the new column name
new_column_name = input("Enter the name for the new column to indicate matches: ")

# List of Metric values to always mark as 'No'
ignore_list = [
    'bms_battery_health.count_battery_voltage',
    'bms_battery_health.count_battery_current',
    'bms_state_limits.count_chrg_status',
    'bms_state_limits.count_chrgr_highest_current',
    'bms_state_limits.count_chrgr_highest_voltage',
    'DC_DC_Conv_OutputCurrent.count__12Vconv_Outputcurrent'
]

# Run the function to compare and update
compare_and_update(file1_path, file2_path, output_file_path, new_column_name, ignore_list)
