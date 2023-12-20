# import os
# import pandas as pd

# # Set the directory path to traverse
# directory_path = r'C:\Users\PARIDHI\Documents\GDCdata\TCGA-LGG\Transcriptome_Profiling\Gene_Expression_Quantification'

# # Initialize a dictionary to store data from each .tsv file
# data_dict = {}

# # Initialize a set to store unique gene names
# unique_gene_names_set = set()

# # Traverse the directory
# for root, _, files in os.walk(directory_path):
#     for file in files:
#         if file.endswith(".tsv"):
#             file_path = os.path.join(root, file)
#             tsv_data = pd.read_csv(file_path, sep='\t', header=1)  # Specify that the header is in the second row
#             gene_values = tsv_data[['gene_name', 'tpm_unstranded']]
#             unique_gene_names_set.update(gene_values['gene_name'].astype(str))
#             gene_data = gene_values.groupby('gene_name')['tpm_unstranded'].mean().reset_index()
#             data_dict[file] = gene_data.set_index('gene_name')

# # Convert the set to a sorted list
# unique_gene_names = sorted(list(unique_gene_names_set))

# # Create an initial DataFrame with the unique gene names as columns
# merged_data = pd.DataFrame(index=unique_gene_names)

# # Populate the DataFrame with data from each file
# for file, gene_data in data_dict.items():
#     merged_data[file] = gene_data['tpm_unstranded']

# # Fill missing values with 'NONE'
# merged_data = merged_data.fillna('NONE')

# # Save the merged data to an Excel file
# output_excel_file = "output_lgg.xlsx"
# merged_data.to_excel(output_excel_file)

# print(f"Data saved to {output_excel_file}")





import openpyxl

# Define the file path
excel_file = r'C:\Users\PARIDHI\output_lgg.xlsx'

# Define the data to be written
# data_to_write = [
#     "TCGA-CS-4942", 
#     "TCGA-CS-4944", 
#     "TCGA-CS-5393", 
#     "TCGA-CS-5396", 
#     "TCGA-CS-5397", 
#     "TCGA-CS-6186", 
#     "TCGA-CS-6188", 
#     "TCGA-CS-6665", 
#     "TCGA-CS-6666", 
#     "TCGA-CS-6668", 
#     "TCGA-CS-6669", 
#     "TCGA-DU-5851", 
#     "TCGA-DU-5854", 
#     "TCGA-DU-5855", 
#     "TCGA-DU-5872", 
#     "TCGA-DU-5874", 
#     "TCGA-DU-6404", 
#     "TCGA-DU-6542", 
#     "TCGA-DU-7008", 
#     "TCGA-DU-7010", 
#     "TCGA-DU-7014", 
#     "TCGA-DU-7015", 
#     "TCGA-DU-7018", 
#     "TCGA-DU-7019", 
#     "TCGA-DU-7294", 
#     "TCGA-DU-7298", 
#     "TCGA-DU-7299", 
#     "TCGA-DU-7300", 
#     "TCGA-DU-7301", 
#     "TCGA-DU-7302", 
#     "TCGA-DU-7304", 
#     "TCGA-DU-7306", 
#     "TCGA-DU-7309", 
#     "TCGA-DU-8162", 
#     "TCGA-DU-8164", 
#     "TCGA-DU-8166", 
#     "TCGA-DU-8167", 
#     "TCGA-DU-8168", 
#     "TCGA-DU-A5TR", 
#     "TCGA-DU-A5TS", 
#     "TCGA-DU-A5TT", 
#     "TCGA-DU-A5TU", 
#     "TCGA-DU-A5TW", 
#     "TCGA-DU-A5TY", 
#     "TCGA-DU-A6S7", "TCGA-DU-A6S8", "TCGA-FG-5964", 
#     "TCGA-FG-6689", "TCGA-FG-6691", "TCGA-FG-6692", 
#     "TCGA-FG-7634", "TCGA-FG-A4MT", "TCGA-HT-7473", 
#     "TCGA-HT-7602", "TCGA-HT-7680", "TCGA-HT-7686", 
#     "TCGA-HT-7690", "TCGA-HT-7694", "TCGA-HT-7879", 
#     "TCGA-HT-7884", "TCGA-HT-8018", "TCGA-HT-8111", 
#     "TCGA-HT-8114", "TCGA-HT-8563", "TCGA-HT-A61A"
# ]
data_to_write = [
    "BraTS20_Training_271",
    "BraTS20_Training_272",
    "BraTS20_Training_273",
    "BraTS20_Training_274",
    "BraTS20_Training_275",
    "BraTS20_Training_276",
    "BraTS20_Training_277",
    "BraTS20_Training_278",
    "BraTS20_Training_279",
    "BraTS20_Training_280",
    "BraTS20_Training_281",
    "BraTS20_Training_282",
    "BraTS20_Training_283",
    "BraTS20_Training_284",
    "BraTS20_Training_285",
    "BraTS20_Training_286",
    "BraTS20_Training_287",
    "BraTS20_Training_288",
    "BraTS20_Training_289",
    "BraTS20_Training_290",
    "BraTS20_Training_291",
    "BraTS20_Training_292",
    "BraTS20_Training_293",
    "BraTS20_Training_294",
    "BraTS20_Training_295",
    "BraTS20_Training_296",
    "BraTS20_Training_297",
    "BraTS20_Training_298",
    "BraTS20_Training_299",
    "BraTS20_Training_300",
    "BraTS20_Training_301",
    "BraTS20_Training_302",
    "BraTS20_Training_303",
    "BraTS20_Training_304",
    "BraTS20_Training_305",
    "BraTS20_Training_306",
    "BraTS20_Training_307",
    "BraTS20_Training_308",
    "BraTS20_Training_309",
    "BraTS20_Training_310",
    "BraTS20_Training_311",
    "BraTS20_Training_312",
    "BraTS20_Training_313",
    "BraTS20_Training_314",
    "BraTS20_Training_315",
    "BraTS20_Training_316",
    "BraTS20_Training_317",
    "BraTS20_Training_318",
    "BraTS20_Training_319",
    "BraTS20_Training_320",
    "BraTS20_Training_321",
    "BraTS20_Training_322",
    "BraTS20_Training_323",
    "BraTS20_Training_324",
    "BraTS20_Training_325",
    "BraTS20_Training_326",
    "BraTS20_Training_327",
    "BraTS20_Training_328",
    "BraTS20_Training_329",
    "BraTS20_Training_330",
    "BraTS20_Training_331",
    "BraTS20_Training_332",
    "BraTS20_Training_333",
    "BraTS20_Training_334",
    "BraTS20_Training_335"
]

# Load the existing Excel file
workbook = openpyxl.load_workbook(excel_file)

# Select the worksheet
worksheet = workbook.active

# Iterate through the data and write it to the first row starting from column 2 (B in Excel)
for index, value in enumerate(data_to_write):
    cell = worksheet.cell(row=1, column=index + 2, value=value)

# Save the modified Excel file
workbook.save(excel_file)