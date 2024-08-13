# Open the input file containing timestamps

dataset_number= 4

input_file = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{dataset_number}/timestamps.txt'
output_file = f'/home/mooo/aub/datasets/aub_zip_video_ficosa_for_HSLAM/ficosa{dataset_number}/times.txt'

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    line_number = 0
    for line in f_in:
        # Remove any leading or trailing whitespace (including newline character) 
        timestamp = line.strip()
        # Format sequence number with leading zeros
        formatted_number = f"{line_number:04}"  # 4 digits with leading zeros
        # Write formatted sequence number followed by timestamp to output file
        f_out.write(f"{formatted_number} {timestamp}\n")
        line_number += 1

print(f"Successfully added formatted sequence numbers to timestamps. Output written to {output_file}")
