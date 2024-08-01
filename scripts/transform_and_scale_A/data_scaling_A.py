#this code scales the hslam and gps data into a 1x1x1 scale

import os
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

# Dataset ID
dataset = 11

# Dictionary to define the second marker index for each data_id
second_marker_indices = {
    0: 20,  # Change this to the desired index for data_id = 0
    1: 500   # Change this to the desired index for data_id = 1
}

def read_data(file_path):
    """Read and parse data from the input file."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            data_id = int(parts[0])
            timestamp = float(parts[1])
            x = float(parts[2])
            y = float(parts[3])
            z = float(parts[4])
            data.append((data_id, timestamp, x, y, z))
    return data

def get_min_max_values(data, data_id):
    """Get the min and max values of x, y, z for a specific data_id."""
    filtered_data = [point for point in data if point[0] == data_id]
    min_x = min(x for _, _, x, _, _ in filtered_data)
    max_x = max(x for _, _, x, _, _ in filtered_data)
    min_y = min(y for _, _, _, y, _ in filtered_data)
    max_y = max(y for _, _, _, y, _ in filtered_data)
    min_z = min(z for _, _, _, _, z in filtered_data)
    max_z = max(z for _, _, _, _, z in filtered_data)
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def normalize_value(value, min_val, max_val):
    """Normalize a value given min and max values."""
    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

def normalize_data(data, scales):
    """Normalize data based on different scales for each data_id."""
    normalized_data = []
    for data_id, timestamp, x, y, z in data:
        (min_x, max_x), (min_y, max_y), (min_z, max_z) = scales[data_id]
        norm_x = normalize_value(x, min_x, max_x)
        norm_y = normalize_value(y, min_y, max_y)
        norm_z = normalize_value(z, min_z, max_z)
        normalized_data.append((data_id, timestamp, norm_x, norm_y, norm_z))
    return normalized_data

def write_data(file_path, data):
    """Write normalized data to the output file."""
    with open(file_path, 'w') as file:
        for data_id, timestamp, x, y, z in data:
            file.write(f"{data_id} {timestamp} {x} {y} {z}\n")

def plot_data_2d(data, output_path):
    """Plot the normalized data for each data_id in 2D and save as HTML."""
    data_id_0 = [point for point in data if point[0] == 0]
    data_id_1 = [point for point in data if point[0] == 1]

    # Create subplots: one row, two columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Data ID = 0", "Data ID = 1"))

    # Function to add traces for a specific data_id
    def add_traces(data_subset, data_id, row, col):
        x_values = [point[2] for point in data_subset]
        y_values = [point[3] for point in data_subset]
        
        # Plot all data points
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers',
            name='All Data Points',
            marker=dict(size=6, color='blue')
        ), row=row, col=col)
        
        # Highlight the first 10 points
        if len(data_subset) > 10:
            x_start_points = [point[2] for point in data_subset[:10]]
            y_start_points = [point[3] for point in data_subset[:10]]
            
            fig.add_trace(go.Scatter(
                x=x_start_points,
                y=y_start_points,
                mode='markers',
                name='First 10 Points',
                marker=dict(size=10, color='red', symbol='cross')
            ), row=row, col=col)
        
        # Highlight the specific point (e.g., 20th point) based on data_id
        second_marker_index = second_marker_indices.get(data_id, -1)  # Default to -1 if not found
        if len(data_subset) > second_marker_index and second_marker_index >= 0:
            x_marker_point = [data_subset[second_marker_index][2]]
            y_marker_point = [data_subset[second_marker_index][3]]
            
            fig.add_trace(go.Scatter(
                x=x_marker_point,
                y=y_marker_point,
                mode='markers',
                name=f'Point at Index {second_marker_index}',
                marker=dict(size=12, color='green', symbol='star')
            ), row=row, col=col)

    # Add traces for data_id = 0
    if data_id_0:
        add_traces(data_id_0, 0, 1, 1)

    # Add traces for data_id = 1
    if data_id_1:
        add_traces(data_id_1, 1, 1, 2)

    fig.update_layout(
        title='2D Plot of Normalized Data',
        xaxis_title='X',
        yaxis_title='Y',
        showlegend=True
    )

    pyo.plot(fig, filename=output_path, auto_open=False)

def plot_data_3d(data, output_path):
    """Plot the normalized data for each data_id in 3D and save as HTML."""
    data_id_0 = [point for point in data if point[0] == 0]
    data_id_1 = [point for point in data if point[0] == 1]

    fig = go.Figure()

    # Plot for data_id = 0
    if data_id_0:
        fig.add_trace(go.Scatter3d(
            x=[point[2] for point in data_id_0],
            y=[point[3] for point in data_id_0],
            z=[point[4] for point in data_id_0],
            mode='lines',
            name='Data ID = 0'
        ))

    # Plot for data_id = 1
    if data_id_1:
        fig.add_trace(go.Scatter3d(
            x=[point[2] for point in data_id_1],
            y=[point[3] for point in data_id_1],
            z=[point[4] for point in data_id_1],
            mode='lines',
            name='Data ID = 1'
        ))

    fig.update_layout(
        title='3D Plot of Normalized Data',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        )
    )

    pyo.plot(fig, filename=output_path, auto_open=False)

# Paths for input and output files
input_file = f"/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz/merged_output_{dataset}.txt"
output_file = f"/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz/merged_output_{dataset}_scaled.txt"

# Create output directories
output_dir = os.path.dirname(output_file)
output_2d_dir = os.path.join(output_dir, "2D")
output_3d_dir = os.path.join(output_dir, "3D")
os.makedirs(output_2d_dir, exist_ok=True)
os.makedirs(output_3d_dir, exist_ok=True)

# Read data from input file
data = read_data(input_file)

# Get min and max values for normalization for each data_id
scales = {
    0: get_min_max_values(data, 0),
    1: get_min_max_values(data, 1)
}

# Normalize the data based on different scales
normalized_data = normalize_data(data, scales)

# Print some sample normalized data for debugging
print("Sample normalized data:")
for i in range(5):
    print(normalized_data[i])

# Write normalized data to output file
write_data(output_file, normalized_data)

# Plot the data
plot_data_2d(normalized_data, os.path.join(output_2d_dir, f"normalized_data_{dataset}_2d.html"))
plot_data_3d(normalized_data, os.path.join(output_3d_dir, f"normalized_data_{dataset}_3d.html"))

print(f"Normalized data has been written to {output_file}")
print(f"2D plot has been saved to {os.path.join(output_2d_dir, f'normalized_data_{dataset}_2d.html')}")
print(f"3D plot has been saved to {os.path.join(output_3d_dir, f'normalized_data_{dataset}_3d.html')}")
