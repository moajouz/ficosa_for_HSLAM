import cv2
import os
import csv

may_dataset = 4

def extract_frames(video_path, output_folder, timestamp_path, output_txt):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Create a list to store the timestamps
    timestamps = []

    # Read the timestamps and frame numbers from the CSV file
    with open(timestamp_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header
        for row in csv_reader:
            timestamp, frame_name = row
            timestamps.append((int(float(timestamp)), frame_name))  # Convert timestamp to integer

    # Output txt file path
    txt_file_path = os.path.join(output_txt, 'timestamps.txt')

    # Check if the timestamps.txt file already exists, and remove it if it does
    if os.path.exists(txt_file_path):
        os.remove(txt_file_path)

    # Write the timestamps to the output txt file
    with open(txt_file_path, 'w') as txt_file:
        for timestamp, _ in timestamps:
            txt_file.write(f"{timestamp}\n")

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    frame_count = 0  # Start the frame count at 0
    
    # Print total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total number of frames in the video: {total_frames}")
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # If the current frame number matches a timestamped frame, save it
        if frame_count < len(timestamps) and f"frame{frame_count+1}" == timestamps[frame_count][1]:
            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Use the timestamp as the file name (integer format)
            output_file_name = f"{timestamps[frame_count][0]}.jpg"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            # Check if the image file already exists, and remove it if it does
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
            
            # Save the grayscale frame as an image file
            cv2.imwrite(output_file_path, gray_frame)
        
        frame_count += 1

    # Release the video capture object
    cap.release()

    print(f"Extracted {frame_count} frames.")

# Example usage
video_path = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{may_dataset}_May/video.mp4'
output_folder = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{may_dataset}_May/frames'
timestamp_path = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{may_dataset}_May/video.csv'
output_txt = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{may_dataset}_May'

extract_frames(video_path, output_folder, timestamp_path, output_txt)
