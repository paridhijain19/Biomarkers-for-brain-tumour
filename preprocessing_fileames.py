

import os
import nibabel as nib
import pandas as pd
from shutil import copyfile
import numpy as np

original_dir = r"C:\Users\PARIDHI\Desktop\MICCAI_BraTS2020_TrainingData"
output_dir = r"C:\Users\PARIDHI\Desktop\Radiomics work\Dataset"
extract_file = r"C:\Users\PARIDHI\Downloads\BraTS Dataset_name_mapping.csv"
output_csv = r"C:\Users\PARIDHI\Desktop\Radiomics work\patient_ids.csv"

if os.path.exists(original_dir):
    for subdir, dirs, files in os.walk(original_dir):
        for file in files:
            if file.endswith("flair.nii.gz") or file.endswith("t1.nii.gz") or file.endswith("t1ce.nii.gz") or file.endswith("t2.nii.gz"):
                from_filepath = subdir + os.path.sep + file
                to_filepath = output_dir + os.path.sep + file
                copyfile(from_filepath,to_filepath)
                print(subdir + os.path.sep + file)
                                
            elif file.endswith("seg.nii.gz"):
                print(subdir + os.path.sep + file)
                from_filepath = subdir + os.path.sep + file
                to_directory = output_dir
                
                seg_file = nib.load(from_filepath)
                flair_seg_data = seg_file.get_fdata()
                flair_seg_data[flair_seg_data != 0] = 1  # whole tumour FLAIR
                flair_data_img = nib.Nifti1Image(flair_seg_data, seg_file.affine, seg_file.header)
                nib.save(flair_data_img,os.path.join(to_directory, file.split('_seg.nii.gz')[0] + '_flair_seg.nii.gz'))             
    
                seg_file = nib.load(from_filepath)
                t2_seg_data = seg_file.get_fdata()
                t2_seg_data[t2_seg_data == 2] = 0  # tumour core T2
                t2_seg_data[t2_seg_data != 0] = 1  # tumour core T2
                t2_data_img = nib.Nifti1Image(t2_seg_data, seg_file.affine, seg_file.header)
                nib.save(t2_data_img,os.path.join(to_directory, file.split('_seg.nii.gz')[0] + '_t2_seg.nii.gz'))
                
                seg_file = nib.load(from_filepath)
                t1ce_seg_data = seg_file.get_fdata()
                t1ce_seg_data[t1ce_seg_data != 4] = 0  # enhanced tumour T1ce
                t1ce_seg_data[t1ce_seg_data == 4] = 1  # enhanced tumour T1ce
                t1ce_data_img = nib.Nifti1Image(t1ce_seg_data, seg_file.affine, seg_file.header)
                nib.save(t1ce_data_img,os.path.join(to_directory, file.split('_seg.nii.gz')[0] + '_t1ce_seg.nii.gz'))
                
                seg_file = nib.load(from_filepath)
                t1_seg_data = seg_file.get_fdata()
                t1_seg_data[t1_seg_data != 1] = 0  # necrotic and non-enhancing tumour core T1
                t1_data_img = nib.Nifti1Image(t1_seg_data, seg_file.affine, seg_file.header)
                nib.save(t1_data_img,os.path.join(to_directory, file.split('_seg.nii.gz')[0] + '_t1_seg.nii.gz'))


df = pd.read_csv(extract_file, usecols=['BraTS_2020_subject_ID', 'Grade'])
df.to_csv('output_csv', index=False)
# list patient ids and their tumour type

patient_ids = [[],[]]
tumour_types = []
tumour_types= pd.read_csv(extract_file, keep_default_na=False)
t_types = tumour_types.iloc[:,0]
#(os.walk(os.path.join(extract_dir))
if os.path.exists(original_dir):
    #tumour_types = next(pd.read_csv(extract_file, keep_default_na=False))[1]
    for each_t in t_types:
        p_ids = next(os.walk(original_dir))[1]
        pre_list = [each_t] * len(p_ids)
        patient_ids[0].extend(p_ids)
        patient_ids[1].extend(pre_list)
        

    
    # export patient ids and corresponding tumour type to csv
    mat = np.matrix(patient_ids).transpose()
    np.savetxt(output_csv, [mat], fmt="%s", delimiter=",")