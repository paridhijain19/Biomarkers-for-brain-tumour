
import numpy as np
import os
import pandas as pd
import pathlib

# pyradiomics provides normalisation in settings therefore we didn't explicitly use standardize() function
def standardize(image):
    """
    Standardize mean and standard deviation 
        of each channel and z_dimension.
    call function as X_norm = standardize(X)

    Args:
        image (np.array): input image, 
            shape (num_channels, dim_x, dim_y, dim_z)

    Returns:
        standardized_image (np.array): standardized version of input image
    """
        
    # initialize to array of zeros, with same shape as the image
    standardized_image = np.zeros(image.shape)
    
    # subtract the mean
    centered = image - np.mean(image)
    # divide by the standard deviation (only if it is different from zero)
    centered_scaled = centered/np.std(centered) if np.std(centered) != 0 else centered
    
    standardized_image = centered_scaled

    return standardized_image

def getImageAndLabelPath(data_dir, p_id, im_type):
    
    # input: data_dir, patient_id, im_type
    # im_type: flair, t1, t1ce, t2
    
    # output: image path and label path
    
    imagePath = os.path.join(data_dir, p_id + '_' + im_type + '.nii.gz')
    labelPath = os.path.join(data_dir, p_id + '_' + im_type + '_seg.nii.gz')
    
    return imagePath, labelPath

def appendAllImagingFeatures(f1, f2, f3, f4):
    f1_df = pd.read_csv(f1)
    f2_df = pd.read_csv(f2)
    f3_df = pd.read_csv(f3)
    f4_df = pd.read_csv(f4)
    
    appended_df = f1_df.append([f2_df, f3_df, f4_df])
    appended_df = appended_df.iloc[:,1:]
    file_path = pathlib.Path(f1)
    folder_path = file_path.parent
    appended_df.to_csv(os.path.join(folder_path, 'appended' + '_features_extraction.csv'), sep=',')

    return

def performKFoldCV(dataset_df, k_value):
    
    # input: full_dataset as pandas df, k-value for split
    
    k = k_value
    sz = len(dataset_df)
    
    n_test = int(sz/k)
    remainder = sz - n_test
    n_validation = int(remainder/k)
    n_training = remainder - n_validation
    
    for i in range(500):
        # here we can add condition to select n HGG and n LGG samples
        test_set = dataset_df.sample(n_test, replace=False)
        n_HGG = test_set.TumourType.str.count("HGG").sum()
        n_LGG = test_set.TumourType.str.count("LGG").sum()
        if n_HGG > int(n_test/2) and n_LGG > int(n_test/3):
            break
        else:
            continue
        
    remainder_set = dataset_df[~dataset_df.isin(test_set).all(1)]
    
    for i in range(500):
        # here we can add condition to select n HGG and n LGG samples
        validation_set = remainder_set.sample(n_validation, replace=False)
        n_HGG = validation_set.TumourType.str.count("HGG").sum()
        n_LGG = validation_set.TumourType.str.count("LGG").sum()
        if n_HGG > int(n_test/2) and n_LGG > int(n_test/3):
            break
        else:
            continue
    
    training_set = remainder_set[~remainder_set.isin(validation_set).all(1)]
    
    return training_set, validation_set, test_set

def splitXY(training_set, validation_set, test_set):
    
    train_x = training_set.loc[:, training_set.columns != 'TumourType']
    train_y = training_set.loc[:, training_set.columns == 'TumourType']
    
    valid_x = validation_set.loc[:, validation_set.columns != 'TumourType']
    valid_y = validation_set.loc[:, validation_set.columns == 'TumourType']
    
    test_x = test_set.loc[:, test_set.columns != 'TumourType']
    test_y = test_set.loc[:, test_set.columns == 'TumourType']
    
    train_y = np.ravel(train_y.replace(['HGG','LGG'],[0,1]))
    valid_y = np.ravel(valid_y.replace(['HGG','LGG'],[0,1]))
    test_y = np.ravel(test_y.replace(['HGG','LGG'],[0,1]))
    
    return train_x, train_y, valid_x, valid_y, test_x, test_y

## a good example for k-fold split
# Import train_test_split function
# from sklearn.cross_validation import train_test_split
# Split dataset into features and labels
# X=data[['petal length', 'petal width','sepal length']]  # Removed feature "sepal length"
# y=data['species']                                       
# Split dataset into training set and test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=5) # 70% training and 30% test