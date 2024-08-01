import numpy as np

datasetnumber = 5

def read_data(file_path):
    """
    Reads data from the given file and returns two lists of corresponding points,
    along with all the original lines for output.
    """
    slam_points = []
    gps_points = []
    all_lines = []  # Store all data lines
    
    with open(file_path, 'r') as f:
        previous_line = None
        for line in f:
            # Store each line to all_lines
            all_lines.append(line.strip())
            
            if previous_line is not None:
                prev_id, prev_timestamp, prev_x, prev_y, prev_z = previous_line.split()
                curr_id, curr_timestamp, curr_x, curr_y, curr_z = line.split()
                
                # Check if previous line was SLAM and current line is GPS
                if int(prev_id) == 0 and int(curr_id) == 1:
                    slam_points.append([float(prev_x), float(prev_y), float(prev_z)])
                    gps_points.append([float(curr_x), float(curr_y), float(curr_z)])
                    
            previous_line = line    
    
    return np.array(slam_points), np.array(gps_points), all_lines

def compute_transformation(slam_points, gps_points):
    """
    Computes the translation, rotation, and scale factor between two sets of corresponding points.
    """
    centroid_slam = np.mean(slam_points, axis=0)
    centroid_gps = np.mean(gps_points, axis=0)
    
    translation_vector = np.array([0.0, 0.0, 0.0])

    centered_slam = slam_points - centroid_slam
    centered_gps = gps_points - centroid_gps
    
    H = np.dot(centered_slam.T, centered_gps)
    U, S, Vt = np.linalg.svd(H)
    R_matrix = np.dot(Vt.T, U.T)
    
    if np.linalg.det(R_matrix) < 0:
        Vt[-1, :] *= -1
        R_matrix = np.dot(Vt.T, U.T)
    
    # Compute scale factor (try both variations if needed)
    # scale_factor = np.sum(distances_slam) / np.sum(distances_gps)
    scale_factor = np.sum(np.linalg.norm(centered_gps, axis=1)) / np.sum(np.linalg.norm(centered_slam, axis=1))
    
    return translation_vector, R_matrix, scale_factor

def apply_transformation(gps_point, translation_vector, R_matrix, scale_factor):
    """
    Applies the computed transformation to a single GPS point.
    """
    return scale_factor * np.dot(gps_point, R_matrix.T) + translation_vector

def transform_and_output_data(file_path, output_path):
    """
    Reads the data, computes the transformation, and outputs the transformed data
    to a new file.
    """
    # Step 3: Identify Corresponding Points and read all data
    slam_points, gps_points, all_lines = read_data(file_path)
    
    # Check that we have enough points
    if len(slam_points) == 0 or len(gps_points) == 0:
        print("No corresponding points found.")
        return
    
    # Step 4: Determine Transformation Parameters
    translation_vector, R_matrix, scale_factor = compute_transformation(slam_points, gps_points)
    
    # Step 5: Apply the Transformation and output all data
    with open(output_path, 'w') as output_file:
        for line in all_lines:
            id, timestamp, x, y, z = line.split()
            if int(id) == 1:  # GPS point
                # Apply transformation to GPS point
                gps_point = np.array([float(x), float(y), float(z)])
                transformed_point = apply_transformation(gps_point, translation_vector, R_matrix, scale_factor)
                # Write transformed GPS point
                output_file.write(f"1 {timestamp} {transformed_point[0]} {transformed_point[1]} {transformed_point[2]}\n")
            else:
                # Write SLAM data without modification
                output_file.write(f"{line}\n")

if __name__ == "__main__":
    input_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz/merged_output_{datasetnumber}.txt'  # Input file path
    output_file =  f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz_transformed_and_scaled/merged_output_{datasetnumber}_transformed_and_scaled.txt'  # Output file path
    
    # Remove the contents of the output file if it already exists
    open(output_file, 'w').close()
    
    transform_and_output_data(input_file, output_file)
    print(f'done {datasetnumber}')
