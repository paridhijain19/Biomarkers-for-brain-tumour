

import os
import pandas as pd
import numpy as np

# same as radiomics_features.py file; choose from ['flair','t1','t1ce','t2']
im_types = ['t1', 't1ce', 't2','flair']

# reduce highly correlated features from each im_type features dataframe
i = 0
for im_type in im_types:
    patient_ids_file = r'C:\Users\PARIDHI\Desktop\Radiomics work\patient_ids.csv'
    s1 = r'C:\Users\PARIDHI\Desktop\Radiomics work'
    s2 = im_type + '_features_extraction.csv'
    im_type_features_file = os.path.join(s1,s2)
    
    im_type_features_df = pd.read_csv(im_type_features_file, keep_default_na=False)
    im_type_features_df = im_type_features_df.replace(r'', np.nan, regex=True)
    im_type_features_df = im_type_features_df.dropna(axis=1, how='any')
    im_type_features_dataset = im_type_features_df.iloc[:,1:].transpose()
    df_header = im_type_features_dataset.iloc[0]
    im_type_features_dataset = im_type_features_dataset[1:]
    im_type_features_dataset.columns = df_header
    patient_ids_df = pd.read_csv(patient_ids_file, header=None)
    patient_ids_df.columns = ['PatientID', 'TumourType']
    p_ids_df = patient_ids_df.set_index('PatientID')
    
    im_type_full_dataset = pd.concat([im_type_features_dataset, p_ids_df], axis=1, join='inner')
    im_type_features_df = im_type_full_dataset
    im_type_features_df = im_type_features_df.drop(columns=['TumourType'])
    im_type_features_df = im_type_features_df.astype(float)
    im_type_correlations = im_type_features_df.corr(method='pearson')
    
    im_type_cor_matrix = im_type_correlations
    temp_df = im_type_features_df
    upper_tri = im_type_cor_matrix.where(np.triu(np.ones(im_type_cor_matrix.shape),k=1).astype(bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
    im_type_final_df = temp_df.drop(columns=to_drop)
    
    if i==0:
        im_type_reduced_features_df = im_type_final_df
        i = 1
    else:
        im_type_reduced_features_df = pd.concat([im_type_reduced_features_df, im_type_final_df], axis=1, join='inner')        
    print(f'\n Highly correlated {len(to_drop)} {im_type} features are omitted!')
    
# reduce highly correlated features from the combined dataframes of all im_type features dataframe

overall_correlations = im_type_reduced_features_df.corr(method='pearson')
overall_cor_matrix = overall_correlations
temp_df2 = im_type_reduced_features_df
upper_tri = overall_cor_matrix.where(np.triu(np.ones(overall_cor_matrix.shape),k=1).astype(bool))
to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
overall_reduced_features_df = temp_df2.drop(columns=to_drop)
print(f'\n Highly correlated {len(to_drop)} features are omitted from combined features dataframes! \n')
print(f'\n Overall {np.size(overall_reduced_features_df,1)} features are preserved for further analysis! \n')

# merge Tumour Type and export overall_reduced_features_df as csv

overall_full_reduced_dataset = pd.concat([overall_reduced_features_df, p_ids_df], axis=1, join='inner')
overall_full_reduced_dataset.to_csv(os.path.join(s1,'overall_reduced_features_copy.csv'), sep=',')