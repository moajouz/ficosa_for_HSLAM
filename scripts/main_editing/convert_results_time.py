def process_data(input_file, output_file):
    # Open the input file for reading and the output file for writing
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Process each line in the input file
        for line in infile: 
            # Split the line into individual values
            values = line.split()
            # Convert the first column to a 16-digit integer
            first_value = int(float(values[0]) * 1e-3)
            # Reconstruct the line with the new first value and the remaining original values
            processed_line = f"{first_value} " + " ".join(values[1:]) + "\n"
            # Write the processed line to the output file
            outfile.write(processed_line)

# Specify the input and output file paths
input_file = '/home/mooo/HSLAM/build/result.txt'
output_file = '/home/mooo/aub/datasets/ficosa_for_HSLAM/HSLAM_Results/Hslam_ficosa_11.txt'
 
# Run the processing function
process_data(input_file, output_file)

# Inform the user about the output file creation
print(f"Processing complete. Output saved to {output_file}")
