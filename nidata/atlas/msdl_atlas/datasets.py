# *- encoding: utf-8 -*-
"""
Utilities to download NeuroImaging-based atlases
"""
# Author: Alexandre Abraham, Philippe Gervais
# License: simplified BSD

import os

from sklearn.datasets.base import Bunch

from ...core.datasets import HttpDataset


class MSDLDataset(HttpDataset):
    """Download and load the MSDL brain atlas.

    Parameters
    ----------
    data_dir: string, optional
        Path of the data directory. Used to force data storage in a specified
        location. Default: None

    url: string, optional
        Override download URL. Used for test only (or if you setup a mirror of
        the data).

    Returns
    -------
    data: sklearn.datasets.base.Bunch
        Dictionary-the interest attributes are :
        - 'labels': str. Path to csv file containing labels.
        - 'maps': str. path to nifti file containing regions definition.

    """
    def fetch(self, url=None, resume=True, verbose=1):
        url = 'https://team.inria.fr/parietal/files/2015/01/MSDL_rois.zip'
        opts = {'uncompress': True}

        dataset_name = "msdl_atlas"
        files = [(os.path.join('MSDL_rois', 'msdl_rois_labels.csv'), url, opts),
                 (os.path.join('MSDL_rois', 'msdl_rois.nii'), url, opts)]
        files = self.fetcher.fetch(files, force=not resume, verbose=verbose)
        return Bunch(labels=files[0], maps=files[1])


def fetch_msdl_atlas(data_dir=None, url=None, resume=True, verbose=1):
    return MSDLDataset(data_dir=data_dir).fetch(url=url, resume=resume, verbose=verbose)
