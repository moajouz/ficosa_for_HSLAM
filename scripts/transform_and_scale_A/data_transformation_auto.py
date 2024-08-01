#this is an automatic transformation to transform all data

import numpy as np
datasetnumber = 11
# Define the input and output file paths
input_file_path =  f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_scaled/merged_output_{datasetnumber}_scaled.txt'

output_file_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_transformed_auto/merged_output_{datasetnumber}_transformed_auto.txt'


# Placeholder transformation parameters (should be determined from data)
R = np.eye(3)  # Rotation matrix (identity for placeholder)
t = np.array([0, 0, 0])  # Translation vector (zero for placeholder)
s = 1.0  # Scale factor (1.0 for placeholder)

# Function to apply transformation
def transform_slam_data(point):
    return s * R.dot(point) + t

# Read data from the input file
data = []

with open(input_file_path, 'r') as file:
    for line in file:
        data_id, timestamp, x, y, z = line.split()
        data_id = int(data_id)
        timestamp = float(timestamp)
        point = np.array([float(x), float(y), float(z)])
        data.append((data_id, timestamp, point))

# Placeholder for actual transformation calculation
# This example uses placeholder values for R, t, and s

# Transform SLAM data
transformed_data = []
for data_id, timestamp, point in data:
    if data_id == 0:  # SLAM data
        transformed_point = transform_slam_data(point)
        transformed_data.append((data_id, timestamp, transformed_point))
    else:  # GPS data
        transformed_data.append((data_id, timestamp, point))

# Sort data by timestamp
transformed_data.sort(key=lambda x: x[1])

# Write to the output file
with open(output_file_path, 'w') as file:
    for data_id, timestamp, point in transformed_data:
        file.write(f"{data_id} {timestamp} {point[0]} {point[1]} {point[2]}\n")

print(f"Transformed data written to {output_file_path}")
