import pandas as pd
import argparse
import os

def merge_csvs(control_file, treatment_file, output_folder, data_type):
    """
    This function merges two CSV files and renames the columns.

    Parameters:
        control_file (str): Path to the control CSV file.
        treatment_file (str): Path to the treatment CSV file.
        output_folder (str): Path to the output folder.
        data_type (str): Type of data ("transcriptome" or "genome").

    Returns:
        A Pandas DataFrame containing the merged data.
    """
    
    # Use os.path.join to create full paths for control and treatment files
    control_file = os.path.abspath(control_file)
    treatment_file = os.path.abspath(treatment_file)

    # Read the two CSV files into DataFrames
    control = pd.read_csv(control_file, sep=",")
    treatment = pd.read_csv(treatment_file, sep=",")
    
    if data_type == "transcriptome":
        # Split the "transcript_ID" column into multiple columns
        columns_to_split = ["ID", "gene_id", "havana_gene", "havana_transcript", "transcript_name", "gene_name", "ontology_id", "RNA_feature", "Direction"]
        control[columns_to_split] = control["ID"].str.split(",", expand=True)
        treatment[columns_to_split] = treatment["ID"].str.split(",", expand=True)
        
        # Merge the two DataFrames based on transcriptome columns
        merge_new = pd.merge(
            control, treatment, on=[
                "ID", "gene_id", "havana_gene", "havana_transcript",
                "transcript_name", "gene_name", "ontology_id", "RNA_feature",
                "Direction", "position", "base_type"
            ]
        )
        
        # Select the desired columns for transcriptome
        desired_columns = [
            "ID", "gene_id", "havana_gene", "havana_transcript",
            "transcript_name", "gene_name", "ontology_id", "RNA_feature",
            "Direction", "position", "base_type", "control_coverage",
            "control_misC", "control_C_reads", "control_T_reads", "treatment_coverage",
            "treatment_misC", "treatment_C_reads", "treatment_T_reads"
        ]
        
    elif data_type == "genome":
        # Merge the two DataFrames based on genome columns
        merge_new = pd.merge(
            control, treatment, on=[
                "ID", "position", "base_type"
            ]
        )
        
        # Select the desired columns for genome
        desired_columns = [
            "ID", "position", "base_type", "control_coverage",
            "control_misC", "control_C_reads", "control_T_reads", "treatment_coverage",
            "treatment_misC", "treatment_C_reads", "treatment_T_reads"
        ]
    else:
        raise ValueError("Invalid data_type. Use 'transcriptome' or 'genome'.")
       
    # Select the desired columns
    merge_new = merge_new[desired_columns]

    # Use drop_duplicates() to remove any duplicated rows
    merge_new = merge_new[desired_columns].drop_duplicates()
    
    # Generate the output filename based on input filenames
    control_basename = os.path.splitext(os.path.basename(control_file))[0]
    treatment_basename = os.path.splitext(os.path.basename(treatment_file))[0]
    output_filename = f"{control_basename}_vs_{treatment_basename}.csv"
    output_path = os.path.join(output_folder, output_filename)
    
    # Write the merged DataFrame to a new CSV file
    merge_new.to_csv(output_path, index=False)
    

    # Return the merged DataFrame
    return merge_new

#if __name__ == "__main__":
#     # Create argument parser
#     parser = argparse.ArgumentParser(description="Merge two CSV files.")
#     parser.add_argument('-c', '--control-file', required=True, help="Path to the control CSV file")
#     parser.add_argument('-t', '--treatment-file', required=True, help="Path to the treatment CSV file")
#     parser.add_argument('-o', '--output-folder', required=True, help="Path to the output folder")
#     parser.add_argument('-d', '--data-type', choices=['transcriptome', 'genome'], required=True, help="Type of data (transcriptome or genome)")
#     args = parser.parse_args()

#     # Run the function with command-line arguments
#     merge_new = merge_csvs(args.control_file, args.treatment_file, args.output_folder, args.data_type)
    
#     # Print the merged DataFrame
#     print(merge_new)
