import numpy as np
from scipy.spatial.transform import Rotation as R

datasetnumber = 5
destination = '_my_scale_and_transformation'

def read_data(file_path):
    slam_points = []
    gps_points = []
    timestamps = []

    try:
        with open(file_path, 'r') as f:
            previous_line = None
            for line in f:
                if previous_line is not None:
                    prev_id, prev_timestamp, prev_x, prev_y, prev_z = previous_line.split()
                    curr_id, curr_timestamp, curr_x, curr_y, curr_z = line.split()
                    
                    if int(prev_id) == 0 and int(curr_id) == 1:
                        slam_points.append([float(prev_x), float(prev_y), float(prev_z)])
                        gps_points.append([float(curr_x), float(curr_y), float(curr_z)])
                        # Convert timestamps to integers
                        timestamps.append(int(float(prev_timestamp)))  # Convert float timestamp to int
                        timestamps.append(int(float(curr_timestamp)))  # Convert float timestamp to int
                        
                previous_line = line
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        raise
    except ValueError:
        print(f"Error: File {file_path} contains invalid data.")
        raise

    return np.array(slam_points), np.array(gps_points), np.array(timestamps)

def compute_scaling_factors(slam_points, gps_points):
    s_x = (gps_points[:, 0].max() - gps_points[:, 0].min()) / (slam_points[:, 0].max() - slam_points[:, 0].min()) if slam_points[:, 0].max() != slam_points[:, 0].min() else 1
    s_y = (gps_points[:, 1].max() - gps_points[:, 1].min()) / (slam_points[:, 1].max() - slam_points[:, 1].min()) if slam_points[:, 1].max() != slam_points[:, 1].min() else 1
    s_z = (gps_points[:, 2].max() - gps_points[:, 2].min()) / (slam_points[:, 2].max() - slam_points[:, 2].min()) if slam_points[:, 2].max() != slam_points[:, 2].min() else 1

    return np.array([s_x, s_y, s_z])

def scale_slam_points(slam_points, scaling_factors):
    return slam_points * scaling_factors

def get_centroid(slam_points, gps_points):
    centroid_slam = np.mean(slam_points, axis=0)
    centroid_gps = np.mean(gps_points, axis=0)

    return centroid_slam, centroid_gps

def compute_rotation_matrix(scaled_slam_points, gps_points):
    centroid_slam, centroid_gps = get_centroid(scaled_slam_points, gps_points)

    scaled_slam_centered = scaled_slam_points - centroid_slam
    gps_centered = gps_points - centroid_gps

    H = np.dot(scaled_slam_centered.T, gps_centered)

    U, _, Vt = np.linalg.svd(H)
    R_matrix = np.dot(Vt.T, U.T)
    
    if np.linalg.det(R_matrix) < 0:
        Vt[-1, :] *= -1
        R_matrix = np.dot(Vt.T, U.T)

    return R.from_matrix(R_matrix)

def transform_slam_points(scaled_slam_points, rotation, centroid_slam, translation_vector):
    rotation_matrix = rotation.as_matrix()
    rotated_points = np.dot(scaled_slam_points - centroid_slam, rotation_matrix.T)
    return rotated_points + translation_vector

if __name__ == "__main__":
    input_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz/merged_output_{datasetnumber}.txt'
    output_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/Scale_B/Merged_results_GPS_xyz{destination}/merged_output_{datasetnumber}{destination}.txt'
  
    slam_points, gps_points, timestamps = read_data(input_path)

    scaling_factors = compute_scaling_factors(slam_points, gps_points)
    scaled_slam_points = scale_slam_points(slam_points, scaling_factors)

    rotation = compute_rotation_matrix(scaled_slam_points, gps_points)
    centroid_slam, centroid_gps = get_centroid(slam_points, gps_points)
    translation_vector = centroid_gps - np.mean(np.dot(scaled_slam_points, rotation.as_matrix().T), axis=0)
    transformed_slam_points = transform_slam_points(scaled_slam_points, rotation, centroid_slam, translation_vector)

    try:
        with open(output_path, 'w') as output_file:
            for i in range(len(timestamps) // 2):
                timestamp_slam = timestamps[2 * i]
                timestamp_gps = timestamps[2 * i + 1]
                coordinates_slam = transformed_slam_points[i]
                coordinates_gps = gps_points[i]
                output_file.write(f"0 {timestamp_slam} {coordinates_slam[0]:.6f} {coordinates_slam[1]:.6f} {coordinates_slam[2]:.6f}\n")
                output_file.write(f"1 {timestamp_gps} {coordinates_gps[0]:.6f} {coordinates_gps[1]:.6f} {coordinates_gps[2]:.6f}\n")
    except IOError:
        print(f"Error: Unable to write to file {output_path}.")
        raise

    print(f"Transformation complete. Scale factors: {scaling_factors}")
    print(f"Rotation matrix:\n{rotation.as_matrix()}")
    print(f"Translation vector: {translation_vector}")
