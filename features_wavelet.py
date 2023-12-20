

from utils import standardize, getImageAndLabelPath
import pandas as pd
import radiomics
from radiomics import featureextractor
import SimpleITK as sitk
import os
import numpy as np

parent_dir = r'C:\Users\PARIDHI\Desktop\Radiomics work'
data_dir = r'C:\Users\PARIDHI\Desktop\Radiomics work\Dataset'
patient_ids_file = r"C:\Users\PARIDHI\Desktop\Radiomics work\patient_ids.csv"

patient_ids_and_types = pd.read_csv(patient_ids_file, header=None)
patient_ids = patient_ids_and_types.iloc[:,0]

# to set up feature extraction
settings = {}
settings['interpolator'] = sitk.sitkBSpline
settings['normalize'] = True  # pyradiomics provides normalisation in settings, therefore, we didn't explicitly use standardize() function
settings['label'] = 1
extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
# extractor.disableAllFeatures()
extractor.enableAllFeatures()
# extractor.enableFeatureClassByName('firstorder')   

im_filter = 'original' # note that, this is not a part of the settings. it is used to create pd dataframe of features
im_types = ['t1','t1ce', 't2', 'flair'] # select from flair, t1, t1ce, t2

# to perform feature extraction
for im_type in im_types: 
    each_im_type_all_p_ids_features_df = pd.DataFrame()
    for p_id in patient_ids: 
        imageName, maskName = getImageAndLabelPath(data_dir, p_id, im_type)
        
        print(f'\n Calculating features for patient id {p_id} \n')
        try:
            featureVector = extractor.execute(imageName, maskName)
        except ValueError:
            each_im_type_all_p_ids_features_df[p_id] = np.nan
            continue
        else:
            if p_id == patient_ids[0]:
                for featureName in featureVector.keys():
                    print("A sample of feature extraction... \n")
                    print("Computed %s: %s" % (featureName, featureVector[featureName]))

            list_of_features = []
            for featureName in featureVector.keys():
                if featureName.find(im_filter) == 0:
                    l = [im_type + '_' + featureName, featureVector[featureName]]
                    list_of_features.append(l)
            
            each_im_type_each_p_id_features_df = pd.DataFrame(list_of_features)
            each_im_type_each_p_id_features_df.columns = ['FeatureName', str(p_id)]
            each_im_type_each_p_id_features_df.set_index('FeatureName')
            
            if each_im_type_all_p_ids_features_df.empty:
                
                each_im_type_each_p_id_features_df.to_csv(os.path.join(parent_dir,'sample_feature_wavelet_extraction.csv'), sep=',')
                each_im_type_all_p_ids_features_df = pd.DataFrame(each_im_type_each_p_id_features_df)
                each_im_type_all_p_ids_features_df.set_index('FeatureName')
            else:
                df1 = each_im_type_all_p_ids_features_df
                df2 = each_im_type_each_p_id_features_df[p_id]
                each_im_type_all_p_ids_features_df = pd.concat([df1, df2], axis=1, join='inner') 
    
    each_im_type_all_p_ids_features_df.to_csv(os.path.join(parent_dir, im_type + '_features_extraction.csv'), sep=',')
    print(f'\n Feature extraction in {im_type} images is completed for all patients! \n')
    
    del each_im_type_all_p_ids_features_df, each_im_type_each_p_id_features_df

print('\n All features have been extracted! \n')
