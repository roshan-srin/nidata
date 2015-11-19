# *- encoding: utf-8 -*-
"""
Utilities to download functional MRI datasets
"""
# Author: Alexandre Abraham, Philippe Gervais
# License: simplified BSD

import os

from sklearn.datasets.base import Bunch

from ...core.datasets import HttpDataset


class Miyawaki2008Dataset(HttpDataset):
    """Download and loads Miyawaki et al. 2008 dataset (153MB)
    No content to run.
    Returns
    -------
    data: Bunch
        Dictionary-like object, the interest attributes are :
        'func': string list
            Paths to nifti file with bold data
        'label': string list
            Paths to text file containing session and target data
        'mask': string
            Path to nifti mask file to define target volume in visual
            cortex

    """
    def fetch(self, url=None, resume=True, force=False, verbose=1):

        url = 'https://www.nitrc.org/frs/download.php' \
              '/5899/miyawaki2008.tgz?i_agree=1&download_now=1'
        opts = {'uncompress': True}

        # Dataset files

        # Functional MRI:
        #   * 20 random scans (usually used for training)
        #   * 12 figure scans (usually used for testing)

        func_figure = [(os.path.join('func', 'data_figure_run%02d.nii.gz' % i),
                        url, opts) for i in range(1, 13)]

        func_random = [(os.path.join('func', 'data_random_run%02d.nii.gz' % i),
                        url, opts) for i in range(1, 21)]

        # Labels, 10x10 patches, stimuli shown to the subject:
        #   * 20 random labels
        #   * 12 figure labels (letters and shapes)

        label_filename = 'data_%s_run%02d_label.csv'
        label_figure = [(os.path.join('label', label_filename % ('figure', i)),
                         url, opts) for i in range(1, 13)]

        label_random = [(os.path.join('label', label_filename % ('random', i)),
                         url, opts) for i in range(1, 21)]

        # Masks

        file_mask = [
            'mask.nii.gz',
            'LHlag0to1.nii.gz',
            'LHlag10to11.nii.gz',
            'LHlag1to2.nii.gz',
            'LHlag2to3.nii.gz',
            'LHlag3to4.nii.gz',
            'LHlag4to5.nii.gz',
            'LHlag5to6.nii.gz',
            'LHlag6to7.nii.gz',
            'LHlag7to8.nii.gz',
            'LHlag8to9.nii.gz',
            'LHlag9to10.nii.gz',
            'LHV1d.nii.gz',
            'LHV1v.nii.gz',
            'LHV2d.nii.gz',
            'LHV2v.nii.gz',
            'LHV3A.nii.gz',
            'LHV3.nii.gz',
            'LHV4v.nii.gz',
            'LHVP.nii.gz',
            'RHlag0to1.nii.gz',
            'RHlag10to11.nii.gz',
            'RHlag1to2.nii.gz',
            'RHlag2to3.nii.gz',
            'RHlag3to4.nii.gz',
            'RHlag4to5.nii.gz',
            'RHlag5to6.nii.gz',
            'RHlag6to7.nii.gz',
            'RHlag7to8.nii.gz',
            'RHlag8to9.nii.gz',
            'RHlag9to10.nii.gz',
            'RHV1d.nii.gz',
            'RHV1v.nii.gz',
            'RHV2d.nii.gz',
            'RHV2v.nii.gz',
            'RHV3A.nii.gz',
            'RHV3.nii.gz',
            'RHV4v.nii.gz',
            'RHVP.nii.gz'
        ]

        file_mask = [(os.path.join('mask', m), url, opts) for m in file_mask]

        file_names = func_figure + func_random + label_figure + label_random
        file_names += file_mask

        files = self.fetcher.fetch(file_names, resume=resume, force=force, verbose=verbose)

        # Return the data
        return Bunch(
            func=files[:32],
            label=files[32:64],
            mask=files[64],
            mask_roi=files[65:])


def fetch_miyawaki2008(data_dir=None, url=None, resume=True, verbose=1):
    return Miyawaki2008Dataset(data_dir=data_dir).fetch(url=url,
                                                        resume=resume,
                                                        verbose=verbose)
