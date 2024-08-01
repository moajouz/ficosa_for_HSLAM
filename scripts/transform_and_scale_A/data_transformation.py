#this is a manual transformation that rotates the slam data around the x-axis then translates it up-warde by 1 on the y-axis, this should be done after using scale_A

import pandas as pd
import numpy as np

# Define the dataset number
datasetnumber = 11

# Define file paths using dataset number
merged_output_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_scaled/merged_output_{datasetnumber}_scaled.txt'
transformed_output_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_transformed/merged_output_{datasetnumber}_transformed.txt'

# Read merged output file
merged_data = pd.read_csv(merged_output_file, delim_whitespace=True, header=None, names=['id', 'timestamp', 'x', 'y', 'z'])

# Separate data for hslam and gps
hslam_data = merged_data[merged_data['id'] == 0]
gps_data = merged_data[merged_data['id'] == 1]

# Rotate HSLAM data by 180 degrees around the x-axis
def rotate_x_180(data):
    # Rotation matrix for 180 degrees around the x-axis
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ])
    # Apply rotation
    coords = data[['x', 'y', 'z']].values
    rotated_coords = coords @ rotation_matrix.T
    rotated_df = pd.DataFrame(rotated_coords, columns=['x', 'y', 'z'])
    rotated_df['timestamp'] = data['timestamp'].values  # Keep timestamps
    rotated_df['id'] = 0  # Ensure id is 0 for HSLAM data
    return rotated_df

# Translate HSLAM data by shifting y-axis by 1
def translate_y(data, shift=1):
    data['y'] = data['y'] + shift  # Shift y-coordinates by 1 unit
    return data

# Process HSLAM data with rotation and translation
hslam_data_transformed = translate_y(rotate_x_180(hslam_data))

# Combine the GPS data with the transformed HSLAM data
combined_data = pd.concat([
    gps_data,  # Original GPS data
    hslam_data_transformed  # Transformed HSLAM data
])

# Sort combined data by timestamp
combined_data_sorted = combined_data.sort_values(by='timestamp').reset_index(drop=True)

# Save combined data to a new file
combined_data_sorted.to_csv(transformed_output_file, sep=' ', header=False, index=False)

print("Transformations applied and transformed data file saved successfully.")
