
import os
import pandas as pd
import SimpleITK as sitk
import numpy as np

def dataset_dataframe(path_main_folder):

    df = pd.DataFrame(columns=['File','Path']) #TODO: Add PatientID in dataframe
    for root, dirs, files in os.walk(path_main_folder):
        if root.endswith('MRS1'):
            paths = [os.path.join(root, filename) for filename in files]

        else:
            paths = [os.path.join(root, filename) for filename in files]

        df1 = pd.DataFrame({'File': files, 'Path': paths})
        df = df.append(df1)

    #df['PatientID'] = df['Path'].map(lambda x: x.lstrip('/'))

    df = df.sort_index()
    df = df[~df['File'].astype(str).str.startswith('._')] #Removes filenames starting with ._ (due to copying of files)

    return df



df = dataset_dataframe('/Volumes/Untitled/LARC_T2_cleaned_nii')
#df = dimensions('/Volumes/Untitled 1/Ingvild_Oxytarget')


def dimensions(dataset_dataframe):
    dataset_dataframe['ImageDimension'] = ''
    for i, row in dataset_dataframe.iterrows():
        image = sitk.ReadImage(row[1])
        array = sitk.GetArrayFromImage(image)
        dim = np.shape(array)
        print(dim)
        dataset_dataframe.at['ImageDimension'] = dim
    return dataset_dataframe

dimensions(df)