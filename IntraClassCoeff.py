

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform

#import pingouin as pg

# selct appropriate feature file
features_file = r'C:\Users\PARIDHI\Desktop\Radiomics work\all_features.csv'
patient_ids_file = r'C:\Users\PARIDHI\Desktop\Radiomics work\patient_ids.csv'

features_df = pd.read_csv(features_file, keep_default_na=False)
features_df = features_df.replace(r'', np.nan, regex=True)
features_df = features_df.dropna(axis=1, how='any')
features_dataset = features_df.iloc[:,1:].transpose()
df_header = features_dataset.iloc[0]
features_dataset = features_dataset[1:]
features_dataset.columns = df_header

patient_ids_df = pd.read_csv(patient_ids_file, header=None)
patient_ids_df.columns = ['PatientID', 'TumourType']
p_ids_df = patient_ids_df.set_index('PatientID')

full_dataset = pd.concat([features_dataset, p_ids_df], axis=1, join='inner')

features_df = full_dataset
features_df = features_df.drop(columns=['TumourType'])

# calculate ICC to see if there is poor(<0.5), moderate(>0.5 and <0.75), good (>0.75 and <0.9), or excellent (>0.9) reliability among features
#https://pingouin-stats.org/generated/pingouin.intraclass_corr.html

icc_df = features_df
icc_df = icc_df.astype(float)
icc_df = icc_df.reset_index()
icc_long_df = pd.melt(icc_df, id_vars='index', value_vars=icc_df.columns)
icc_long_df = icc_long_df.rename(columns={"index": "P_ID", "variable":"FeatureName", "value":"FeatureValue"})

icc_mat = pg.intraclass_corr(data=icc_long_df, targets='P_ID', raters='FeatureName', ratings='FeatureValue')
icc_mat = icc_mat.set_index('Type')
icc_mat


# visualise correlation matrix to see what features have high correlation

# correlation coefficient
plt.figure(figsize=(60,40), dpi=600)
features_df = features_df.astype(float)
correlations = features_df.corr(method='pearson')
corr_fig = sns.heatmap(round(correlations,2), cmap='PiYG', vmin=-1, vmax=1);
corr_fig.figure.savefig(os.path.join(r'C:\Users\PARIDHI\Desktop\Radiomics work\figures', 'tt_corr.png'))

#plt.figure(figsize=(60,40), dpi=600)
dissimilarity = 1 - np.abs(correlations)
s = squareform(dissimilarity)
s = np.clip(s,0,1)
Z = linkage(s, 'complete')
dendrogram(Z, labels=features_df.columns, orientation='top', 
           leaf_rotation=90);
plt.savefig(os.path.join(r'C:\Users\PARIDHI\Desktop\Radiomics work\figures', 'tt_dend.png'))

# clusterise data using threshold

# identifying correct threshold by visualising correlation heatmaps corresponding to multiple thresholds
plt.figure(figsize=(15,10))

for idx, t in enumerate(np.arange(0.2,1.1,0.1)):
    
    # Subplot idx + 1
    plt.subplot(3, 3, idx+1)
    
    # Calculate the cluster
    labels = fcluster(Z, t, criterion='distance')

    # Keep the indices to sort labels
    labels_order = np.argsort(labels)

    # Build a new dataframe with the sorted columns
    for idx, i in enumerate(features_df.columns[labels_order]):
        if idx == 0:
            clustered = pd.DataFrame(features_df[i])
        else:
            df_to_append = pd.DataFrame(features_df[i])
            clustered = pd.concat([clustered, df_to_append], axis=1)
            
    # Plot the correlation heatmap
    correlations = clustered.corr()
    sns.heatmap(round(correlations,2), cmap='Blues', vmin=-1, vmax=1, 
                xticklabels=False, yticklabels=False)
    plt.title("Threshold = {}".format(round(t,2)))
           
# clusterise the data                      
threshold = 0.7
labels = fcluster(Z, threshold, criterion='distance')
labels_order = np.argsort(labels)

for idx, i in enumerate(features_df.columns[labels_order]):
    if idx == 0:
        clustered = pd.DataFrame(features_df[i])
    else:
        df_to_append = pd.DataFrame(features_df[i])
        clustered = pd.concat([clustered, df_to_append], axis=1)

#plt.figure(figsize=(60,40), dpi=600)
correlations = clustered.corr()
corr_clustered_fig = sns.heatmap(round(correlations,2), cmap='Blues', vmin=-1, vmax=1);
corr_clustered_fig.figure.savefig(os.path.join(r'C:\Users\PARIDHI\Desktop\Radiomics work\figures', 'tt_corr_clustered.png'))

# plot clustermap and correlation heatmap together
sns.set(font_scale=7)
corr_cluster_fig = sns.clustermap(correlations, method="complete", tree_kws=dict(linewidths=4.5), row_cluster=False, cmap='Blues', vmin=-1, vmax=1, figsize=(60,80), yticklabels=False, xticklabels=5);
corr_cluster_fig.savefig(os.path.join(r"C:\Users\PARIDHI\Desktop\Radiomics work\figures", 'corr_cluster.png'), bbox_inches='tight', dpi=300)
