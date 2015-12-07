# *- encoding: utf-8 -*-
"""
Utilities to download NeuroImaging-based atlases
"""
# Author: Alexandre Abraham, Philippe Gervais
# License: simplified BSD

from sklearn.datasets.base import Bunch

from ...core.datasets import HttpDataset


class Craddock2012Dataset(HttpDataset):
    """Download and return file names for the Craddock 2012 parcellation
    Parameters
    ----------
    data_dir: string

    url: string

    Returns
    -------
    data: sklearn.datasets.base.Bunch
        dictionary-like object, keys are:
        scorr_mean, tcorr_mean

    References
    ----------
    Licence: Creative Commons Attribution Non-commercial Share Alike
    http://creativecommons.org/licenses/by-nc-sa/2.5/

    Craddock, R. Cameron, G.Andrew James, Paul E. Holtzheimer, Xiaoping P. Hu,
    and Helen S. Mayberg. "A Whole Brain fMRI Atlas Generated via Spatially
    Constrained Spectral Clustering". Human Brain Mapping 33, no 8 (2012):
    1914–1928. doi:10.1002/hbm.21333.

    See http://www.nitrc.org/projects/cluster_roi/ for more information
    on this parcellation.
    """

    def fetch(self, url=None, resume=True, force=False, verbose=1):

        if url is None:
            url = "ftp://www.nitrc.org/home/groups/cluster_roi/htdocs" \
                  "/Parcellations/craddock_2011_parcellations.tar.gz"
        opts = {'uncompress': True}

        dataset_name = "craddock_2012"
        keys = ("scorr_mean", "tcorr_mean",
                "scorr_2level", "tcorr_2level",
                "random")
        filenames = [
                ("scorr05_mean_all.nii.gz", url, opts),
                ("tcorr05_mean_all.nii.gz", url, opts),
                ("scorr05_2level_all.nii.gz", url, opts),
                ("tcorr05_2level_all.nii.gz", url, opts),
                ("random_all.nii.gz", url, opts)
        ]

        sub_files = self.fetcher.fetch(filenames, resume=resume,
                                       force=force, verbose=verbose)

        params = dict(list(zip(keys, sub_files)))

        return Bunch(**params)


def fetch_craddock_2012_atlas(data_dir=None, url=None, resume=True, verbose=1):
    return Craddock2012Dataset(data_dir=data_dir).fetch(url=url, resume=resume, verbose=verbose)

