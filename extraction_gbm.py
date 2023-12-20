import os
import pandas as pd

# Set the directory path to traverse
directory_path = r'C:\Users\PARIDHI\Documents\GDCdata'

# Initialize a dictionary to store data from each .tsv file
data_dict = {}

# Initialize a set to store unique gene names
unique_gene_names_set = set()

# Traverse the directory
for root, _, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".tsv"):
            file_path = os.path.join(root, file)
            tsv_data = pd.read_csv(file_path, sep='\t', header=1)  # Specify that the header is in the second row
            gene_values = tsv_data[['gene_name', 'tpm_unstranded']]
            unique_gene_names_set.update(gene_values['gene_name'].astype(str))
            gene_data = gene_values.groupby('gene_name')['tpm_unstranded'].mean().reset_index()
            data_dict[file] = gene_data.set_index('gene_name')

# Convert the set to a sorted list
unique_gene_names = sorted(list(unique_gene_names_set))

# Create an initial DataFrame with the unique gene names as columns
merged_data = pd.DataFrame(index=unique_gene_names)

# Populate the DataFrame with data from each file
for file, gene_data in data_dict.items():
    merged_data[file] = gene_data['tpm_unstranded']

# Fill missing values with 'NONE'
merged_data = merged_data.fillna('NONE')

# Save the merged data to an Excel file
output_excel_file = "output_combined.csv"
merged_data.to_excel(output_excel_file)

print(f"Data saved to {output_excel_file}")


# # import openpyxl

# # # Define the file path
# # excel_file = r'C:\Users\PARIDHI\output_gbm.xlsx'

# # # Define the data to be written
# # data_to_write = [
#     "BraTS20_Training_166",
#     "BraTS20_Training_182", 
#     "BraTS20_Training_184", 
#     "BraTS20_Training_185", 
#     "BraTS20_Training_190", 
#     "BraTS20_Training_197", 
#     "BraTS20_Training_199", 
#     "BraTS20_Training_201", 
#     "BraTS20_Training_203", 
#     "BraTS20_Training_205", 
#     "BraTS20_Training_206", 
#     "BraTS20_Training_209", 
#     "BraTS20_Training_210", 
#     "BraTS20_Training_211", 
#     "BraTS20_Training_212", 
#     "BraTS20_Training_226", 
#     "BraTS20_Training_233", 
#     "BraTS20_Training_236", 
#     "BraTS20_Training_240", 
#     "BraTS20_Training_245", 
#     "BraTS20_Training_246"
# # ]

# # # Load the existing Excel file
# # workbook = openpyxl.load_workbook(excel_file)

# # # Select the worksheet
# # worksheet = workbook.active

# # # Iterate through the data and write it to the first row starting from column 2 (B in Excel)
# # for index, value in enumerate(data_to_write):
# #     cell = worksheet.cell(row=1, column=index + 2, value=value)

# # # Save the modified Excel file
# # workbook.save(excel_file)


