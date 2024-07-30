import unittest
import pandas as pd
import os

# Function to be tested (simplified for context)
def compare_and_update(file1_path, file2_path, output_file_path, new_column_name, ignore_list):
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

class TestCSVComparison(unittest.TestCase):

    def setUp(self):
        """Set up test files and paths."""
        self.file1_path = 'test_file1.csv'
        self.file2_path = 'test_file2.csv'
        self.output_file_path = 'output_test_file.csv'
        self.new_column_name = 'Presence'
        self.ignore_list = [
            'bms_battery_health.count_battery_voltage',
            'bms_battery_health.count_battery_current',
            'bms_state_limits.count_chrg_status',
            'bms_state_limits.count_chrgr_highest_current',
            'bms_state_limits.count_chrgr_highest_voltage'
        ]

    def create_test_files(self, content1, content2):
        """Helper method to create test CSV files."""
        pd.DataFrame(content1).to_csv(self.file1_path, index=False)
        pd.DataFrame(content2).to_csv(self.file2_path, index=False)

    def test_basic_functionality(self):
        """Test basic functionality of comparing metrics."""
        content1 = {'Metric': ['metric1', 'metric2', 'metric3']}
        content2 = {'Metric': ['metric2', 'metric4']}
        expected_output = {'Metric': ['metric1', 'metric2', 'metric3'], 'Presence': ['No', 'Yes', 'No']}

        self.create_test_files(content1, content2)
        compare_and_update(self.file1_path, self.file2_path, self.output_file_path, self.new_column_name, self.ignore_list)
        
        result_df = pd.read_csv(self.output_file_path)
        expected_df = pd.DataFrame(expected_output)

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_ignore_list(self):
        """Test that metrics in the ignore list are always marked 'No'."""
        content1 = {'Metric': [
            'bms_battery_health.count_battery_voltage',
            'metric3',
            'bms_battery_health.count_battery_current'
        ]}
        content2 = {'Metric': ['bms_battery_health.count_battery_voltage', 'metric4']}
        expected_output = {'Metric': [
            'bms_battery_health.count_battery_voltage',
            'metric3',
            'bms_battery_health.count_battery_current'
        ], 'Presence': ['No', 'No', 'No']}

        self.create_test_files(content1, content2)
        compare_and_update(self.file1_path, self.file2_path, self.output_file_path, self.new_column_name, self.ignore_list)

        result_df = pd.read_csv(self.output_file_path)
        expected_df = pd.DataFrame(expected_output)

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_special_logic(self):
        """Test special logic for controller metrics."""
        content1 = {'Metric': [
            'controller_motor_status_1_REAR',
            'controller_motor_status_2_FRONT'
        ]}
        content2 = {'Metric': [
            'controller_motor_status_1_REAR.count_motorcontroller_1_controller_temp',
            'controller_motor_status_2_FRONT.count_motorcontroller_2_controller_temp'
        ]}
        expected_output = {'Metric': [
            'controller_motor_status_1_REAR',
            'controller_motor_status_2_FRONT'
        ], 'Presence': ['Yes', 'Yes']}

        self.create_test_files(content1, content2)
        compare_and_update(self.file1_path, self.file2_path, self.output_file_path, self.new_column_name, self.ignore_list)

        result_df = pd.read_csv(self.output_file_path)
        expected_df = pd.DataFrame(expected_output)

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_empty_files(self):
        """Test behavior with empty CSV files."""
        content1 = {'Metric': []}
        content2 = {'Metric': []}
        expected_output = {'Metric': [], 'Presence': []}

        self.create_test_files(content1, content2)
        compare_and_update(self.file1_path, self.file2_path, self.output_file_path, self.new_column_name, self.ignore_list)

        result_df = pd.read_csv(self.output_file_path)
        expected_df = pd.DataFrame(expected_output)

        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_missing_metric_column(self):
        """Test behavior when 'Metric' column is missing."""
        content1 = {'NotMetric': ['metric1']}
        content2 = {'Metric': ['metric2']}
        pd.DataFrame(content1).to_csv(self.file1_path, index=False)
        pd.DataFrame(content2).to_csv(self.file2_path, index=False)

        with self.assertRaises(KeyError):
            compare_and_update(self.file1_path, self.file2_path, self.output_file_path, self.new_column_name, self.ignore_list)

    def tearDown(self):
        """Remove test files after each test."""
        try:
            os.remove(self.file1_path)
            os.remove(self.file2_path)
            os.remove(self.output_file_path)
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()
