#This is the working scale, it scales hslam to the size of gps

import numpy as np

datasetnumber = 5

slam_points = []
gps_points = []
all_lines = []

def min_max_assignment(arr_val, compval):
    if compval > arr_val[1]:
        arr_val[1] = compval
    if compval < arr_val[0]:
        arr_val[0] = compval

def read_data(file_path):
    """
    Reads data from the given file and returns two lists of corresponding points,
    along with all the original lines for output.
    """
   
    gps_x = [float('inf'), float('-inf')]
    gps_y = [float('inf'), float('-inf')]
    gps_z = [float('inf'), float('-inf')]
    slam_x = [float('inf'), float('-inf')]
    slam_y = [float('inf'), float('-inf')]
    slam_z = [float('inf'), float('-inf')]
    
    with open(file_path, 'r') as f:
        for line in f:
            # Store each line to all_lines
            all_lines.append(line.strip())
            id, timestamp, X, Y, Z = line.split()

            x, y, z = float(X), float(Y), float(Z)
            # Check if previous line was SLAM and current line is GPS
            if int(id) == 0:
                slam_points.append([x, y, z])                
                min_max_assignment(slam_x, x)
                min_max_assignment(slam_y, y)
                min_max_assignment(slam_z, z)

            else:
                gps_points.append([x, y, z])
                min_max_assignment(gps_x, x)
                min_max_assignment(gps_y, y)
                min_max_assignment(gps_z, z)

    return np.array(slam_points), np.array(gps_points), all_lines, (gps_x, gps_y, gps_z, slam_x, slam_y, slam_z)

def scale_data(file_path):
    # Read the data and extract relevant points and min/max bounds
    slam, gps, data, (gps_x, gps_y, gps_z, slam_x, slam_y, slam_z) = read_data(file_path)
    
    # Calculate scaling factors
    scale_x = (gps_x[1] - gps_x[0]) / (slam_x[1] - slam_x[0])
    scale_y = (gps_y[1] - gps_y[0]) / (slam_y[1] - slam_y[0])
    scale_z = (gps_z[1] - gps_z[0]) / (slam_z[1] - slam_z[0])
    
    scaled_slam_points = slam * np.array([scale_x, scale_y, scale_z])

    # Return the scaled SLAM points and the scale factors
    return scaled_slam_points

if __name__ == "__main__":
    input_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz/merged_output_{datasetnumber}.txt'  # Input file path
    output_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_my_scale/merged_output_{datasetnumber}_my_scale.txt'  # Output file path
    
    # Remove the contents of the output file if it already exists
    open(output_path, 'w').close()
    
    scaled_slam_points = scale_data(input_path)

    with open(output_path, 'w') as output_file:
        slam_idx = 0
        for line in all_lines:
            id, timestamp, x, y, z = line.split()
            if int(id) == 0:  # SLAM point
                # Use the corresponding scaled point
                transformed_point = scaled_slam_points[slam_idx]
                slam_idx += 1
                # Write transformed SLAM point
                output_file.write(f"0 {timestamp} {transformed_point[0]:.6f} {transformed_point[1]:.6f} {transformed_point[2]:.6f}\n")
            else:
                # Write GPS data without modification
                output_file.write(f"{line}\n")

    print(f"Scale factors: {scaled_slam_points}")
