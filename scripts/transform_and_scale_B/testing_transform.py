#ignore

import numpy as np

def compute_transformation(slam_points, gps_points):
    """
    Computes the translation, rotation, and scale factor to align SLAM points with GPS points.
    """
    # Calculate centroids of both point sets
    centroid_slam = np.mean(slam_points, axis=0)
    centroid_gps = np.mean(gps_points, axis=0)

    # Compute the translation vector from SLAM to GPS
    translation_vector = centroid_gps - centroid_slam

    # Center the points by subtracting their centroids
    centered_slam = slam_points - centroid_slam
    centered_gps = gps_points - centroid_gps

    # Compute the covariance matrix H
    H = np.dot(centered_slam.T, centered_gps)

    # Singular Value Decomposition (SVD)
    U, S, Vt = np.linalg.svd(H)
    R_matrix = np.dot(Vt.T, U.T)

    # Ensure the rotation matrix is proper
    if np.linalg.det(R_matrix) < 0:
        Vt[-1, :] *= -1
        R_matrix = np.dot(Vt.T, U.T)

    # Calculate the scale factor
    scale_factor = np.sum(np.linalg.norm(centered_gps, axis=1)) / np.sum(np.linalg.norm(centered_slam, axis=1))

    return translation_vector, R_matrix, scale_factor

def apply_transformation(slam_point, translation_vector, R_matrix, scale_factor):
    """
    Applies the computed transformation to a single SLAM point to align with GPS.
    """
    return scale_factor * np.dot(R_matrix, slam_point.T).T + translation_vector

if __name__ == "__main__":
    # Example SLAM and GPS points
    slam_points = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0]
    ])
    
    gps_points = np.array([
        [1.5, 2.5, 3.5],
        [4.5, 5.5, 6.5],
        [7.5, 8.5, 9.5]
    ])

    # Compute the transformation
    translation_vector, R_matrix, scale_factor = compute_transformation(slam_points, gps_points)
    
    print("Translation Vector:", translation_vector)
    print("Rotation Matrix:\n", R_matrix)
    print("Scale Factor:", scale_factor)
    
    # Apply transformation and display transformed SLAM points
    print("\nTransformed SLAM Points:")
    for slam_point in slam_points:
        transformed_point = apply_transformation(slam_point, translation_vector, R_matrix, scale_factor)
        print(f"Original: {slam_point}, Transformed: {transformed_point}")
