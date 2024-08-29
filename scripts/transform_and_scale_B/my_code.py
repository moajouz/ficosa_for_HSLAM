#this transfroms all data as it is

import numpy as np
from scipy.spatial.transform import Rotation as R

datasetnumber = '4_may'
destination = 'Transformed_manual'

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
                        timestamps.append(int(float(prev_timestamp)))
                        timestamps.append(int(float(curr_timestamp)))
                        
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

def compute_rotation_matrix(scaled_slam_points, gps_points):
    centroid_slam, centroid_gps = np.mean(scaled_slam_points, axis=0), np.mean(gps_points, axis=0)
    scaled_slam_centered = scaled_slam_points - centroid_slam
    gps_centered = gps_points - centroid_gps

    H = np.dot(scaled_slam_centered.T, gps_centered)

    U, _, Vt = np.linalg.svd(H)
    R_matrix = np.dot(Vt.T, U.T)
    
    if np.linalg.det(R_matrix) < 0:
        Vt[-1, :] *= -1
        R_matrix = np.dot(Vt.T, U.T)

    return R.from_matrix(R_matrix)

def rotate_slam_points(scaled_slam_points, rotation):
    rotation_matrix = rotation.as_matrix()
    return np.dot(scaled_slam_points, rotation_matrix.T)

def get_translation_vector(transformed_slam_points, gps_points):
    translation_vector = gps_points[0] - transformed_slam_points[0]
    return translation_vector

def transform_slam_point(slam, scale, rotation, translation):
    # Reshape the SLAM point to a 2D array for matrix operations
    scaled_slam = scale_slam_points(slam.reshape(1, -1), scale)
    
    # Apply rotation
    rotated_slam = rotate_slam_points(scaled_slam, rotation)
    
    # Apply translation and flatten to convert back to 1D array
    transformed_slam = rotated_slam + translation
    return transformed_slam.flatten()

if __name__ == "__main__":
    input_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/Merged_results/merged_output_{datasetnumber}.txt'
    output_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/{destination}/merged_output_{datasetnumber}.txt'

    # input_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/Merged_results/merged_output_{datasetnumber}.txt'
    # output_path = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/{destination}/merged_output_{datasetnumber}.txt'

    slam_points, gps_points, timestamps = read_data(input_path)

    scaling_factors = compute_scaling_factors(slam_points, gps_points)
    scaled_slam_points = scale_slam_points(slam_points, scaling_factors)
    rotation = compute_rotation_matrix(scaled_slam_points, gps_points)
    transformed_slam_points = rotate_slam_points(scaled_slam_points, rotation)
    translation_vector = get_translation_vector(transformed_slam_points, gps_points)
    
    output = []
    modified_coordinate = []

    try:
        with open(input_path, 'r') as f:
            for line in f:
                id, times, x, y, z = line.split()
                
                if int(id) == 0:
                    slam_input_points = np.array([float(x), float(y), float(z)])
                    modified_coordinate = transform_slam_point(slam_input_points, scaling_factors, rotation, translation_vector)
                    output.append([int(id), int(float(times)), modified_coordinate[0], modified_coordinate[1], modified_coordinate[2]])
                else:
                    output.append([int(id), int(float(times)), float(x), float(y), float(z)])

    except FileNotFoundError:
        print(f"Error: The file {input_path} does not exist.")
        raise
    except ValueError:
        print(f"Error: File {input_path} contains invalid data.")
        raise

    try:
        with open(output_path, 'w') as output_file:
            for record in output:
                output_file.write(f"{record[0]} {record[1]} {record[2]:.6f} {record[3]:.6f} {record[4]:.6f}\n")    
    except IOError:
        print(f"Error: Unable to write to file {output_path}.")
        raise

    print(f"Transformation complete. Scale factors: {scaling_factors}")
    print(f"Rotation matrix:\n{rotation.as_matrix()}")
    print(f"translation vector:\n{translation_vector}")
