# merges the gps xyz with hslam in timestamp order

import csv

dataset = '4_may'

# Define a class to store data with IDs
class DataWithID:
    def __init__(self, timestamp, x, y, z, id):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def __repr__(self):
        return f"{self.id} {self.timestamp} {self.x} {self.y} {self.z}"

# Function to load HSLAM data from a text file
def load_hslam_data(txt_file_path):
    hslam_data_vec = []
    try: 
        with open(txt_file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 4:
                    timestamp, x, y, z = map(float, parts[:4])
                    hslam_data_vec.append(DataWithID(timestamp, x, y, z, 0))
    except FileNotFoundError:
        print(f"Failed to open text file: {txt_file_path}")
    return hslam_data_vec

# Function to load GPS data from a CSV file
def load_gps_data(csv_path):
    gps_data_list = []
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header line
            for row in reader:
                if len(row) >= 11:
                    x, y, z = map(float, row[12:15])
                    timestamp = float(row[10])
                    gps_data_list.append(DataWithID(timestamp, x, y, z, 1))
    except FileNotFoundError:
        print(f"Failed to open CSV file: {csv_path}")
    return gps_data_list

def main():
    hslam_file_path = f"/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/HSLAM_Results/Hslam_ficosa_{dataset}.txt"
    gps_file_path = f"/home/mooo/aub/datasets/ficosa_for_HSLAM/FICOSA_trajectories/ficosa{dataset}_odometry.csv"
    output_file_path = f"/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/Merged_results_GPS_xyz/merged_output_{dataset}.txt"

    # Load data
    hslam_data = load_hslam_data(hslam_file_path)
    gps_data = load_gps_data(gps_file_path)

    # Merge data
    all_data = hslam_data + gps_data

    # Sort data by timestamp
    all_data.sort(key=lambda data: data.timestamp)

    # Write merged data to a new text file
    try:
        with open(output_file_path, 'w') as output_file:
            for data in all_data:
                output_file.write(f"{data.id} {data.timestamp} {data.x} {data.y} {data.z}\n")
        print(f"Merged data written to {output_file_path}")
    except FileNotFoundError:
        print(f"Failed to open output file: {output_file_path}")

if __name__ == "__main__":
    main()
