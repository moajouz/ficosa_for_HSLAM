#plotting gps and hslam and ekf results data as 2d and 3d while saving them in respevtive folders

import pandas as pd
import plotly.graph_objects as go
import os

# Define dataset number and destination for old cam
# datasetnumber = 9
# gps_type = '_GPS_xyz'
# destination = '_my_scale_and_transformation'
# source = '/old_camera/Scale_B'

# # Define file paths using dataset number and destination
# merged_output_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Merged_results{gps_type}{destination}/merged_output_{datasetnumber}{destination}.txt'
# ekf_result_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Results_EKF{gps_type}{destination}/ekf_result_{datasetnumber}.txt'
# output_2d_folder = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Results_EKF{gps_type}{destination}/2D_Plots'
# output_3d_folder = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Results_EKF{gps_type}{destination}/3D_Plots'

# Define dataset number and destination for new cam
datasetnumber = '4_may' 
destination = 'Auto_EKF'
source = '/new_camera'

# Define file paths using dataset number and destination
merged_output_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/{destination}/merged_output_{datasetnumber}.txt'
ekf_result_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/{destination}/ekf_result_{datasetnumber}.txt'
output_2d_folder = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/{destination}/2D_Plots'
output_3d_folder = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/{destination}/3D_Plots'

# Read merged output file
merged_data = pd.read_csv(merged_output_file, delim_whitespace=True, header=None, names=['id', 'timestamp', 'x', 'y', 'z'])

# Separate data for hslam and gps
hslam_data = merged_data[merged_data['id'] == 0]
gps_data = merged_data[merged_data['id'] == 1]

# Read EKF result file
with open(ekf_result_file, 'r') as f:
    ekf_data = f.readlines()

# Process EKF data
ekf_timestamps = []
ekf_positions = []
for line in ekf_data:
    line = line.strip()
    if line.startswith('Timestamp'):
        timestamp = float(line.split('Timestamp: ')[1].split(',')[0])
        position = line.split('Position: ')[1].strip('[]').split(', ')
        position = [float(pos) for pos in position]
        ekf_timestamps.append(timestamp)
        ekf_positions.append(position)

# Convert EKF positions to DataFrame
ekf_df = pd.DataFrame(ekf_positions, columns=['x', 'y', 'z'])
ekf_df['timestamp'] = ekf_timestamps

# Plotting function
def plot_data(output_path, is_3d=False):
    fig = go.Figure()

    # Add hslam data
    if is_3d:
        fig.add_trace(go.Scatter3d(x=hslam_data['x'], y=hslam_data['y'], z=hslam_data['z'], mode='markers', name='HSLAM'))
    else:
        fig.add_trace(go.Scatter(x=hslam_data['x'], y=hslam_data['y'], mode='markers', name='HSLAM'))

    # Add GPS data
    if is_3d:
        fig.add_trace(go.Scatter3d(x=gps_data['x'], y=gps_data['y'], z=gps_data['z'], mode='markers', name='GPS'))
    else:
        fig.add_trace(go.Scatter(x=gps_data['x'], y=gps_data['y'], mode='markers', name='GPS'))

    # Add EKF data
    if is_3d:
        fig.add_trace(go.Scatter3d(x=ekf_df['x'], y=ekf_df['y'], z=ekf_df['z'], mode='lines+markers', name='EKF'))
    else:
        fig.add_trace(go.Scatter(x=ekf_df['x'], y=ekf_df['y'], mode='lines+markers', name='EKF'))

    # Set layout
    fig.update_layout(
        title='Sensor Data',
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis' if is_3d else None
        ),
        autosize=True
    )

    # Save plot
    fig.write_html(output_path)

# Create output directories if they don't exist
os.makedirs(output_2d_folder, exist_ok=True)
os.makedirs(output_3d_folder, exist_ok=True)

# Plot and save 2D and 3D plots
plot_data(os.path.join(output_2d_folder, f'result_2d_{datasetnumber}.html'), is_3d=False)
plot_data(os.path.join(output_3d_folder, f'result_3d_{datasetnumber}.html'), is_3d=True)

print(f"Plots generated and saved successfully. number {datasetnumber}")
