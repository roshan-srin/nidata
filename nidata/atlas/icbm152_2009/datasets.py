# *- encoding: utf-8 -*-
"""
Utilities to download NeuroImaging-based atlases
"""
# Author: Alexandre Abraham, Philippe Gervais
# License: simplified BSD

import os

from sklearn.datasets.base import Bunch

from ...core.datasets import HttpDataset


class ICBM152Dataset(HttpDataset):
    """Download and load the ICBM152 template (dated 2009)

    Parameters
    ----------
    data_dir: string, optional
        Path of the data directory. Use to forec data storage in a non-
        standard location. Default: None (meaning: default)
    url: string, optional
        Download URL of the dataset. Overwrite the default URL.
    """

    def fetch(self, url=None, resume=True, force=False, verbose=1):
        if url is None:
            url = "http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/" \
                  "mni_icbm152_nlin_sym_09a_nifti.zip"
        opts = {'uncompress': True}

        keys = ("csf", "gm", "wm",
                "pd", "t1", "t2", "t2_relax",
                "eye_mask", "face_mask", "mask")
        filenames = [(os.path.join("mni_icbm152_nlin_sym_09a", name), url, opts)
                     for name in ("mni_icbm152_csf_tal_nlin_sym_09a.nii",
                                  "mni_icbm152_gm_tal_nlin_sym_09a.nii",
                                  "mni_icbm152_wm_tal_nlin_sym_09a.nii",

                                  "mni_icbm152_pd_tal_nlin_sym_09a.nii",
                                  "mni_icbm152_t1_tal_nlin_sym_09a.nii",
                                  "mni_icbm152_t2_tal_nlin_sym_09a.nii",
                                  "mni_icbm152_t2_relx_tal_nlin_sym_09a.nii",

                                  "mni_icbm152_t1_tal_nlin_sym_09a_eye_mask.nii",
                                  "mni_icbm152_t1_tal_nlin_sym_09a_face_mask.nii",
                                  "mni_icbm152_t1_tal_nlin_sym_09a_mask.nii")]

        sub_files = self.fetcher.fetch(filenames, resume=resume,
                                       force=force, verbose=verbose)

        params = dict(list(zip(keys, sub_files)))
        return Bunch(**params)


def fetch_icbm152_2009(data_dir=None, url=None, resume=True, verbose=1):
    return ICBM152Dataset(data_dir=data_dir).fetch(url=url, resume=resume, verbose=verbose)
