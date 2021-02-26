"""
@author: huynhngoc
"""

import customize_obj


if __name__ == '__main__':
    output_folder = '/Volumes/HARDDISK/MasterThesis/Experiments/LARC/traditional_split/LARC_ID_6/best_result/256/' # change this to the folder you want to store the result
    dataset_file = '/Volumes/HARDDISK/MasterThesis/HDF5_data/traditionalSplit_LARC.h5' # path to the dataset

    predicted_h5 = '/Volumes/HARDDISK/MasterThesis/Experiments/LARC/traditional_split/LARC_ID_6/best_result/prediction.017.h5' # the prediction file you want to calculate the dice

    dice_per_slice = output_folder + 'slice.csv'
    dice_per_patient = output_folder + 'patient.csv'
    merge_file = output_folder + 'merge_images.h5'

    customize_obj.H5MetaDataMapping(
        dataset_file,
        dice_per_slice,
        folds=['val/256'], # change this to ['test'] if you want to calculate the dice of the test prediction
        fold_prefix='',
        dataset_names=['patient_ids']#, 'slice_idx']
    ).post_process()

    customize_obj.H5CalculateFScore(
        predicted_h5,
        dice_per_slice
    ).post_process()

    customize_obj.H5Merge2dSlice(
        predicted_h5,
        dice_per_slice,
        map_column='patient_ids',
        merge_file=merge_file,
        save_file=dice_per_patient
    ).post_process()

    customize_obj.H5CalculateFScore(
        merge_file,
        dice_per_patient,
        map_file=dice_per_patient,
        map_column='patient_ids'
    ).post_process()