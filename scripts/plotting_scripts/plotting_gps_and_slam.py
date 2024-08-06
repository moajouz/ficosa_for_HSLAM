#plotting gps and hslam data as 2d and 3d while saving them in respective folders

import plotly.graph_objs as go
import os

datasetnumber = 5
gps_type = '_GPS_xyz'
destination = '_my_scale_and_transformation'
source = '/Scale_B'

chosen_point_index_GPS = 50  # Example index for the chosen point for GPS
chosen_point_index_SLAM = 30  # Example index for the chosen point for SLAM

# Define the input and output file paths
data_file_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Merged_results{gps_type}{destination}/merged_output_{datasetnumber}{destination}.txt'
output_dir_2d = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Merged_results{gps_type}{destination}/2D'
output_dir_3d = f'/home/mooo/aub/datasets/ficosa_for_HSLAM{source}/Merged_results{gps_type}{destination}/3D'

# Create output directories if they do not exist
os.makedirs(output_dir_2d, exist_ok=True)
os.makedirs(output_dir_3d, exist_ok=True)

# Initialize lists for the 2D and 3D plot data
timestamps_slam, timestamps_gps = [], []
x_coords_slam, y_coords_slam, z_coords_slam = [], [], []
x_coords_gps, y_coords_gps, z_coords_gps = [], [], []

# Read the data from the transformed data file
with open(data_file_path, 'r') as file:
    for line in file:
        data_id, timestamp, x, y, z = line.split()
        data_id = int(data_id)
        timestamp = float(timestamp)
        x, y, z = map(float, (x, y, z))

        if data_id == 0:
            # SLAM data
            timestamps_slam.append(timestamp)
            x_coords_slam.append(x)
            y_coords_slam.append(y)
            z_coords_slam.append(z)
        elif data_id == 1:
            # GPS data
            timestamps_gps.append(timestamp)
            x_coords_gps.append(x)
            y_coords_gps.append(y)
            z_coords_gps.append(z)

def add_marker_points(x_slam, y_slam, z_slam, x_gps, y_gps, z_gps, index_slam, index_gps):
    marker_colors = {
        'first': 'yellow',
        'last': 'red',
        'chosen': 'purple'
    }
    
    # Define marker points for SLAM
    marker_points_slam = [
        {'name': 'First', 'color': marker_colors['first'], 'index': 0},
        {'name': 'Last', 'color': marker_colors['last'], 'index': -1},
        {'name': 'Chosen', 'color': marker_colors['chosen'], 'index': index_slam}
    ]
    
    # Define marker points for GPS
    marker_points_gps = [
        {'name': 'First', 'color': marker_colors['first'], 'index': 0},
        {'name': 'Last', 'color': marker_colors['last'], 'index': -1},
        {'name': 'Chosen', 'color': marker_colors['chosen'], 'index': index_gps}
    ]
    
    traces_2d_slam = []
    traces_3d_slam = []
    traces_2d_gps = []
    traces_3d_gps = []

    # Add markers for SLAM
    for marker_point in marker_points_slam:
        idx = marker_point['index']
        
        if idx == -1:  # Last point case
            idx = len(x_slam) - 1
        
        traces_2d_slam.append(go.Scatter(
            x=[x_slam[idx]],
            y=[y_slam[idx]],
            mode='markers+text',
            text=f"SLAM {marker_point['name']} Point",
            name=f'SLAM {marker_point["name"]} (2D)',
            marker=dict(color=marker_point['color'], symbol='x', size=12),
            textposition="top center"
        ))

        traces_3d_slam.append(go.Scatter3d(
            x=[x_slam[idx]],
            y=[y_slam[idx]],
            z=[z_slam[idx]],
            mode='markers+text',
            text=f"SLAM {marker_point['name']} Point",
            name=f'SLAM {marker_point["name"]} (3D)',
            marker=dict(color=marker_point['color'], symbol='x', size=5),
            textposition="top center"
        ))

    # Add markers for GPS
    for marker_point in marker_points_gps:
        idx = marker_point['index']
        
        if idx == -1:  # Last point case
            idx = len(x_gps) - 1
        
        traces_2d_gps.append(go.Scatter(
            x=[x_gps[idx]],
            y=[y_gps[idx]],
            mode='markers+text',
            text=f"GPS {marker_point['name']} Point",
            name=f'GPS {marker_point["name"]} (2D)',
            marker=dict(color=marker_point['color'], symbol='circle', size=12),
            textposition="top center"
        ))

        traces_3d_gps.append(go.Scatter3d(
            x=[x_gps[idx]],
            y=[y_gps[idx]],
            z=[z_gps[idx]],
            mode='markers+text',
            text=f"GPS {marker_point['name']} Point",
            name=f'GPS {marker_point["name"]} (3D)',
            marker=dict(color=marker_point['color'], symbol='circle', size=5),
            textposition="top center"
        ))

    return traces_2d_slam, traces_3d_slam, traces_2d_gps, traces_3d_gps

# Create 2D scatter plot (x-y) for SLAM and GPS data
trace_2d_slam = go.Scatter(
    x=x_coords_slam,
    y=y_coords_slam,
    mode='markers',
    name='SLAM Data (2D)',
    marker=dict(color='blue')
)

trace_2d_gps = go.Scatter(
    x=x_coords_gps,
    y=y_coords_gps,
    mode='markers',
    name='GPS Data (2D)',
    marker=dict(color='green')
)

# Create 3D scatter plot (x-y-z) for SLAM and GPS data
trace_3d_slam = go.Scatter3d(
    x=x_coords_slam,
    y=y_coords_slam,
    z=z_coords_slam,
    mode='markers',
    name='SLAM Data (3D)',
    marker=dict(color='blue')
)

trace_3d_gps = go.Scatter3d(
    x=x_coords_gps,
    y=y_coords_gps,
    z=z_coords_gps,
    mode='markers',
    name='GPS Data (3D)',
    marker=dict(color='green')
)

# Adding marker points with different chosen indices for SLAM and GPS
traces_2d_slam_marker, traces_3d_slam_marker, traces_2d_gps_marker, traces_3d_gps_marker = add_marker_points(
    x_coords_slam, y_coords_slam, z_coords_slam, 
    x_coords_gps, y_coords_gps, z_coords_gps, 
    chosen_point_index_SLAM, chosen_point_index_GPS
)

# Layout for the 2D plot
layout_2d = go.Layout(
    title='2D Scatter Plot (X-Y)',
    xaxis=dict(title='X'),
    yaxis=dict(title='Y')
)

# Layout for the 3D plot
layout_3d = go.Layout(
    title='3D Scatter Plot (X-Y-Z)',
    scene=dict(
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        zaxis=dict(title='Z')
    )
)

# Create the 2D plot figure and save it
fig_2d = go.Figure(data=[trace_2d_slam] + traces_2d_slam_marker + [trace_2d_gps] + traces_2d_gps_marker, layout=layout_2d)
plot_2d_file_path = os.path.join(output_dir_2d, f'2d_plot_{datasetnumber}.html')
fig_2d.write_html(plot_2d_file_path)

# Create the 3D plot figure and save it
fig_3d = go.Figure(data=[trace_3d_slam] + traces_3d_slam_marker + [trace_3d_gps] + traces_3d_gps_marker, layout=layout_3d)
plot_3d_file_path = os.path.join(output_dir_3d, f'3d_plot_{datasetnumber}.html')
fig_3d.write_html(plot_3d_file_path)

print(f"2D plot saved to {plot_2d_file_path}")
print(f"3D plot saved to {plot_3d_file_path}")
