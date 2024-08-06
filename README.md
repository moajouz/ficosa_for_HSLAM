# Ficosa_for_HSLAM
This repo contains all the work that was done to handle and transform the ficosa dataset to make both gps and hslam odometry compatible. <br/>

Explanation of folders: (the explanation contains [script_name] that handeled the modification, the scripts can be found in the scripts folder) <br/>
1- ficosa{n}: contains the modified timestamps.txt file that was turned into the format of times.txt so it can be read by HSLAM [convert_dataset_time.py] <br/>
2- FICOSA_trajectories: contains the normal GPS trajectory provided by ficosa <br/>
3- HSLAM_Results: contains the modified hslam results using [convert_results_time.py], this was done to modify the result timestamp to match the format of that of the GPS format <br/>
4- Merged_results_GPS_LLA and Merged_results_GPS_xyz: contains all the values from hslam and using the gps LLA and xyz data respectively, the data is sorted by timestamp order and having an ID=0 for HSLAM data and an ID=1 for GPS data.
they were done using [merge_sensor_data.py] and [merge_sensor_data_gps_xyz.py] respectively. <br/>
5- Results_EKF_GPS_LLA and Results_EKF_GPS_xyz: are the ekf results of both Merged_results_GPS_LLA and Merged_results_GPS_xyz. <br/>
||the scripts above are from main_editing <br/>
6- Scale_A: <br/>
  - this is a wrong scale approach so can be ignored <br/>
  a- Merged_results_GPS_xyz_scaled: contains the scaled data into a 1x1x1 scale [data_scaling_A.py] <br/>
  b- Merged_results_GPS_xyz_transformed: rotating around the x-axis and then translating by 1 on the y-axis [data_transformation.py] <br/>
  c- Merged_results_GPS_xyz_transformed_auto: this was done using automatic transformation but still did not work perfectly due to scale issue [data_transformation_auto.py] <br/>
  d- remaining forlders: respective ekf results <br/>
  ||the scripts above are from transform_and_scale_A <br/>
7- Scale_B: <br/>/

!! the remaining scripts in plotting_Scripts/ have the general explanation on the first commented line
