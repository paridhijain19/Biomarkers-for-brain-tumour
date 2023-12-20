
import pandas as pd
import numpy as np
import scipy.stats

radiomics_features_file = r'C:\Users\PARIDHI\Desktop\Radiomics work\features\overall_reduced_features_dataset.csv'
biological_features_file = r"C:\Users\PARIDHI\output_combined.csv"
radiomics_features_list = ["P_ID", "t1_original_glszm_LargeAreaEmphasis", "t1_original_glszm_LargeAreaHighGrayLevelEmphasis", "t1_original_glszm_ZoneVariance", "t1ce_original_firstorder_Range"]

radiomics_features_df = pd.read_csv(radiomics_features_file, keep_default_na=False, on_bad_lines='warn')
radiomics_features_df = radiomics_features_df.replace(r'', np.nan, regex=True)
radiomics_features_df = radiomics_features_df.dropna(axis=1, how='any')
radiomics_features_dataset = radiomics_features_df[radiomics_features_list]
radiomics_features_dataset.set_index('P_ID', inplace=True)

biological_features_df = pd.read_csv(biological_features_file, keep_default_na=False, encoding='latin-1', error_bad_lines=False)
biological_features_df = biological_features_df.replace(r'', np.nan, regex=True)
biological_features_df = biological_features_df.dropna(axis=1, how='any')
biological_features_dataset = biological_features_df.iloc[:,:].transpose()
biological_features_dataset_header = biological_features_dataset.iloc[0]
biological_features_dataset = biological_features_dataset[1:]
biological_features_dataset.columns = biological_features_dataset_header

merged_radiomics_biological_features_df = pd.concat([radiomics_features_dataset, biological_features_dataset], axis=1, join="inner")
merged_radiomics_biological_features_df = merged_radiomics_biological_features_df.astype('float64')

data = merged_radiomics_biological_features_df

#import pandas as pd
#import numpy as np
#import scipy.stats
#
#radiomics_features_file = r'C:\Users\PARIDHI\Desktop\Radiomics work\features\overall_reduced_features_dataset.csv'
#biological_features_file = r"C:\Users\PARIDHI\output_combined.csv"
#radiomics_features_list = ["P_ID", "t1_original_glszm_LargeAreaEmphasis", "t1_original_glszm_LargeAreaHighGrayLevelEmphasis", "t1_original_glszm_ZoneVariance", "t1ce_original_firstorder_Range"]
#
#
#radiomics_features_df = pd.read_csv(radiomics_features_file, keep_default_na=False)
#radiomics_features_df = radiomics_features_df.replace(r'', np.nan, regex=True)
#radiomics_features_df = radiomics_features_df.dropna(axis=1, how='any')
#radiomics_features_dataset = radiomics_features_df[radiomics_features_list]
#radiomics_features_dataset.set_index('P_ID', inplace=True)
#
#
##biological_features_df = pd.read_csv(biological_features_file, keep_default_na=False)
##biological_features_df = pd.read_csv(biological_features_file, keep_default_na=False, encoding='ISO-8859-1')
#biological_features_df = pd.read_csv(biological_features_file, keep_default_na=False, encoding='latin-1')
#biological_features_df = biological_features_df.replace(r'', np.nan, regex=True)
#biological_features_df = biological_features_df.dropna(axis=1, how='any')
#biological_features_dataset = biological_features_df.iloc[:,:].transpose()
#biological_features_dataset_header = biological_features_dataset.iloc[0]
#biological_features_dataset = biological_features_dataset[1:]
#biological_features_dataset.columns = biological_features_dataset_header
#
#merged_radiomics_biological_features_df = pd.concat([radiomics_features_dataset, biological_features_dataset], axis=1, join="inner")
#merged_radiomics_biological_features_df = merged_radiomics_biological_features_df.astype('float64')

#data = merged_radiomics_biological_features_df

# select from radiomics features = t1_original_glszm_LargeAreaEmphasis, t1_original_glszm_LargeAreaHighGrayLevelEmphasis, t1_original_glszm_ZoneVariance, t1ce_original_firstorder_Range
#corr_values = data[data.columns].corr(method='pearson')['t1ce_original_firstorder_Range']

# select each gene column name from the previous step and find correlation and P value
#c, P_value = scipy.stats.pearsonr(data['t1ce_original_firstorder_Range'], data['FSCB'])
#print(c)
#print(P_value)



