# the use of this code is to make the data in the txt files be hslam data followed by gps data and removing any other data that won't be published to the ekf

dataset=1
# Define input and output file names
input_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/Transformed_manual/merged_output_{dataset}.txt'  # Replace with your input file name
output_file = f'/home/mooo/aub/datasets/ficosa_for_HSLAM/new_camera/Transformed_manual_corrolated/merged_output_{dataset}.txt'  # Replace with your desired output file name

# Initialize variables
previous_line = None

# Open input file for reading and output file for writing
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # Iterate through each line in the input file
    for current_line in infile:
        # Check if previous line exists and has id 0
        if previous_line and previous_line.startswith('0'):
            # Check if the current line has id 1
            if current_line.startswith('1'):
                # Write both lines to the output file
                outfile.write(previous_line)
                outfile.write(current_line)
        
        # Update the previous_line variable
        previous_line = current_line

print("Filtered lines have been written to", output_file)
