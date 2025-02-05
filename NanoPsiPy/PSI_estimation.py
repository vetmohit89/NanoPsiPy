#!/usr/bin/env python
import csv
import os

# Function to calculate C_reads and T_reads for each row
def calculate_reads(row, sample_name):
    coverage = float(row["coverage"])
    misC = float(row["misC"])
    C_reads = misC * coverage
    T_reads = coverage - C_reads
    row["{}_coverage".format(sample_name)] = coverage
    row["{}_misC".format(sample_name)] = misC
    row["{}_C_reads".format(sample_name)] = C_reads
    row["{}_T_reads".format(sample_name)] = T_reads

def estimate(sample_name, output_file_name):
    # Get the current directory path
    current_directory = os.getcwd()

    # Input and output file paths
    alignment_folder = os.path.join(current_directory, "alignment")
    input_file = os.path.join(alignment_folder, "features.csv")

    # Columns to extract, including kmer
    columns_to_extract = ["ID", "position", "base_type", "coverage", "kmer", "misC"]

    # Read the input file and extract the desired columns
    data = []
    with open(input_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Replace "|" with "," and strip double quotes from all values
            for key, value in row.items():
                row[key] = value.replace('"', '').replace('|', ',')

            extracted_row = {column: row[column] for column in columns_to_extract}
            data.append(extracted_row)

    # Calculate C_reads and T_reads for each row and append them with prefixes
    for row in data:
        calculate_reads(row, sample_name)

    # Prepare fieldnames, including kmer
    fieldnames = [key for key in data[0].keys() if key not in ["coverage", "misC"]]

    # Check if the output file exists
    if os.path.isfile(output_file_name):
        # Append data to the existing output file
        with open(output_file_name, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header if the file is empty
            if os.path.getsize(output_file_name) == 0:
                writer.writeheader()

            # Write data to the output file
            for row in data:
                row.pop("misC", None)
                row.pop("coverage", None)  # Remove coverage only for writing
                writer.writerow(row)
    else:
        # Create a new output file and write the data
        with open(output_file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Write data to the output file
            for row in data:
                row.pop("misC", None)
                row.pop("coverage", None)  # Remove coverage only for writing
                writer.writerow(row)

    print("Extraction and calculation completed. The updated data (without coverage column) is saved to:", output_file_name)
