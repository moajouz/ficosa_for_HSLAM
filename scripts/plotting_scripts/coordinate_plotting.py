#trying to draw the coordinate system of hslam and gps

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

datasetnumber = 5

def read_first_two_points(file_path):
    """
    Reads the first two valid points from the file for SLAM and GPS datasets.
    """
    slam_points = []
    gps_points = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                id, timestamp, x, y, z = line.split()
                id = int(id)
                point = np.array([float(x), float(y), float(z)])
                
                # Collect first two points for each id
                if id == 0 and len(slam_points) < 2:
                    slam_points.append(point)
                elif id == 1 and len(gps_points) < 3:
                    gps_points.append(point)
                
                # Stop if we have collected two points for both
                if len(slam_points) >= 2 and len(gps_points) >= 3:
                    break
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return np.array(slam_points), np.array(gps_points)

def plot_coordinate_frames(slam_points, gps_points):
    """
    Plots the coordinate frames based on the first two points for SLAM and GPS datasets.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Define a fixed arrow length
    arrow_length = 1.0
    
    # Define the origin as the first point and draw axes towards the second point
    if len(slam_points) == 2:
        origin_slam = slam_points[0]
        direction_slam = slam_points[1] - origin_slam
        
        # Normalize the direction and scale to fixed arrow length
        direction_slam_norm = direction_slam / np.linalg.norm(direction_slam)
        direction_slam_scaled = direction_slam_norm * arrow_length
        
        ax.quiver(*origin_slam, direction_slam_scaled[0], 0, 0, color='r', label='SLAM X', length=arrow_length, arrow_length_ratio=0.1)
        ax.quiver(*origin_slam, 0, direction_slam_scaled[1], 0, color='g', label='SLAM Y', length=arrow_length, arrow_length_ratio=0.1)
        ax.quiver(*origin_slam, 0, 0, direction_slam_scaled[2], color='b', label='SLAM Z', length=arrow_length, arrow_length_ratio=0.1)
    
    if len(gps_points) == 3:
        origin_gps = gps_points[0]
        direction_gps = gps_points[2] - origin_gps
        
        # Normalize the direction and scale to fixed arrow length
        direction_gps_norm = direction_gps / np.linalg.norm(direction_gps)
        direction_gps_scaled = direction_gps_norm * arrow_length
        
        ax.quiver(*origin_gps, direction_gps_scaled[0], 0, 0, color='r', label='GPS X', length=arrow_length, arrow_length_ratio=0.1)
        ax.quiver(*origin_gps, 0, direction_gps_scaled[1], 0, color='g', label='GPS Y', length=arrow_length, arrow_length_ratio=0.1)
        ax.quiver(*origin_gps, 0, 0, direction_gps_scaled[2], color='b', label='GPS Z', length=arrow_length, arrow_length_ratio=0.1)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    input_file = os.path.join('/home/mooo/aub/datasets/ficosa_for_HSLAM/Merged_results_GPS_xyz', f'merged_output_{datasetnumber}.txt')
    slam_points, gps_points = read_first_two_points(input_file)
    
    if len(slam_points) == 2 or len(gps_points) == 2:
        print(f"SLAM Points (id=0): {slam_points}")
        print(f"GPS Points (id=1): {gps_points}")
        plot_coordinate_frames(slam_points, gps_points)
    else:
        print(f"Not enough valid points. SLAM: {len(slam_points)}, GPS: {len(gps_points)}")
