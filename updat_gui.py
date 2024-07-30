import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

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
    try:
        file1_df = pd.read_csv(file1_path)
        file2_df = pd.read_csv(file2_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV files: {e}")
        return
    
    # Check if the necessary columns are present
    if 'Metric' not in file1_df.columns or 'Metric' not in file2_df.columns:
        messagebox.showerror("Error", "Both CSV files must contain a 'Metric' column.")
        return
    
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
    try:
        file1_df.to_csv(output_file_path, index=False)
        messagebox.showinfo("Success", f"Updated file saved to: {output_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save updated CSV file: {e}")

class CSVComparerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Comparer")

        # Variables for file paths and column name
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.new_column_name = tk.StringVar()

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # File 1 Selector
        tk.Label(self.root, text="Select the first CSV file:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.file1_path, width=50).grid(row=0, column=1, padx=10)
        tk.Button(self.root, text="Browse", command=self.browse_file1).grid(row=0, column=2)

        # File 2 Selector
        tk.Label(self.root, text="Select the second CSV file:").grid(row=1, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.file2_path, width=50).grid(row=1, column=1, padx=10)
        tk.Button(self.root, text="Browse", command=self.browse_file2).grid(row=1, column=2)

        # Output File Path
        tk.Label(self.root, text="Enter the output CSV file path:").grid(row=2, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.output_file_path, width=50).grid(row=2, column=1, padx=10)
        tk.Button(self.root, text="Save As", command=self.save_as_file).grid(row=2, column=2)

        # New Column Name
        tk.Label(self.root, text="Enter the new column name:").grid(row=3, column=0, sticky='w')
        tk.Entry(self.root, textvariable=self.new_column_name, width=50).grid(row=3, column=1, padx=10)

        # Process Button
        tk.Button(self.root, text="Process", command=self.process_files).grid(row=4, column=1, pady=10)

    def browse_file1(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        self.file1_path.set(filename)

    def browse_file2(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        self.file2_path.set(filename)

    def save_as_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        self.output_file_path.set(filename)

    def process_files(self):
        # Get user inputs
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        output_file = self.output_file_path.get()
        new_col_name = self.new_column_name.get()

        # Check if inputs are valid
        if not file1 or not file2 or not output_file or not new_col_name:
            messagebox.showwarning("Warning", "Please fill out all fields.")
            return

        # Define the list of Metric values to always mark as 'No'
        ignore_list = [
            'bms_battery_health.count_battery_voltage',
            'bms_battery_health.count_battery_current',
            'bms_state_limits.count_chrg_status',
            'bms_state_limits.count_chrgr_highest_current',
            'bms_state_limits.count_chrgr_highest_voltage'
        ]

        # Run the comparison and update process
        compare_and_update(file1, file2, output_file, new_col_name, ignore_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVComparerGUI(root)
    root.mainloop()
