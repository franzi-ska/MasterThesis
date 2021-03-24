
import numpy as np
from sklearn.preprocessing import StandardScaler
import SimpleITK as sitk
import Preprocessing as p
import useful_functions as uf
import os
import matplotlib.pyplot as plt

def zscore_norm(data):
    """
    Takes in an image as a flatten array, and normalize the data using z-score normalization

    :param data: flatten numpy array
    :return: flatten normalized numpy array
    """

    if (len(np.shape(data))) == 1:
        data = np.expand_dims(data, axis=1)

    scaler = StandardScaler(with_mean=True, with_std=True)
    scaler.fit(data)

    norm_data = scaler.transform(data)

    return norm_data

def reconstruct_normalized_image_array(array, image_size):
    """
    Creates an normalized image from an flatten numpy array.

    :param array: flattened normalized numpy array
    :param image_size: image size
    :return: normalized image
    """
    im = np.reshape(array, image_size)
    im = sitk.GetImageFromArray(im)

    return im

def normalize_all(source_folder, destination_folder, image_filename, mask_filename):
    """
    Normalizes all images in a source folder, and saves the images and masks in a destination folder

    :param source_folder: path to main source folder, containing all the patient folders
    :param destination_folder: path to main destination folder, containing all the patient folders
    :param image_filename: filename of image
    :param mask_filename: filename of mask
    :return: normalized images and masks saved in destination folder
    """

    df = p.create_dataframe(source_folder, image_filename, mask_filename)
    dst_paths = uf.create_dst_paths(destination_folder)

    for i in range(len(df['imagePaths'])):
        print('Normalizing:', df['imagePaths'][i])
        array, image_size = uf.get_array_from_image(df['imagePaths'][i])
        norm_array = zscore_norm(array)

        norm_image = reconstruct_normalized_image_array(norm_array, image_size)
        mask = sitk.ReadImage(df['maskPaths'][i])

        sitk.WriteImage(norm_image, os.path.join(dst_paths[i], image_filename))
        sitk.WriteImage(mask, os.path.join(dst_paths[i], mask_filename))

#normalize_all('/Volumes/LaCie/MasterThesis_Ingvild/LARC_cropped', '/Volumes/LaCie/MasterThesis_Ingvild/LARC_cropped_ZScoreNorm', 'image.nii', '1 RTSTRUCT LARC_MRS1-label.nii')
#normalize_all('/Volumes/LaCie/MasterThesis_Ingvild/Oxy_cropped_corrected', '/Volumes/LaCie/MasterThesis_Ingvild/Oxy_cropped_ZScoreNorm', 'T2.nii', 'Manual_an.nii')



