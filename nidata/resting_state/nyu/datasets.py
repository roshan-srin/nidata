# *- encoding: utf-8 -*-
"""
Utilities to download resting state MRI datasets
"""
# Author: Alexandre Abraham, Philippe Gervais
# License: simplified BSD

import os

from sklearn.datasets.base import Bunch

from ...core.datasets import HttpDataset


class NyuRestDataset(HttpDataset):
    """Download and loads the NYU resting-state test-retest dataset.

    Parameters
    ----------
    n_subjects: int, optional
        The number of subjects to load. If None is given, all the
        subjects are used.

    sessions: iterable of int, optional
        The sessions to load. Load only the first session by default.

    data_dir: string, optional
        Path of the data directory. Used to force data storage in a specified
        location. Default: None
    """

    def fetch(self, n_subjects=None, sessions=[1], resume=True,
              force=False, verbose=1):

        fa1 = 'http://www.nitrc.org/frs/download.php/1071/NYU_TRT_session1a.tar.gz'
        fb1 = 'http://www.nitrc.org/frs/download.php/1072/NYU_TRT_session1b.tar.gz'
        fa2 = 'http://www.nitrc.org/frs/download.php/1073/NYU_TRT_session2a.tar.gz'
        fb2 = 'http://www.nitrc.org/frs/download.php/1074/NYU_TRT_session2b.tar.gz'
        fa3 = 'http://www.nitrc.org/frs/download.php/1075/NYU_TRT_session3a.tar.gz'
        fb3 = 'http://www.nitrc.org/frs/download.php/1076/NYU_TRT_session3b.tar.gz'
        fa1_opts = {'uncompress': True,
                    'move': os.path.join('session1', 'NYU_TRT_session1a.tar.gz')}
        fb1_opts = {'uncompress': True,
                    'move': os.path.join('session1', 'NYU_TRT_session1b.tar.gz')}
        fa2_opts = {'uncompress': True,
                    'move': os.path.join('session2', 'NYU_TRT_session2a.tar.gz')}
        fb2_opts = {'uncompress': True,
                    'move': os.path.join('session2', 'NYU_TRT_session2b.tar.gz')}
        fa3_opts = {'uncompress': True,
                    'move': os.path.join('session3', 'NYU_TRT_session3a.tar.gz')}
        fb3_opts = {'uncompress': True,
                    'move': os.path.join('session3', 'NYU_TRT_session3b.tar.gz')}

        p_anon = os.path.join('anat', 'mprage_anonymized.nii.gz')
        p_skull = os.path.join('anat', 'mprage_skullstripped.nii.gz')
        p_func = os.path.join('func', 'lfo.nii.gz')

        subs_a = ['sub05676', 'sub08224', 'sub08889', 'sub09607', 'sub14864',
                  'sub18604', 'sub22894', 'sub27641', 'sub33259', 'sub34482',
                  'sub36678', 'sub38579', 'sub39529']
        subs_b = ['sub45463', 'sub47000', 'sub49401', 'sub52738', 'sub55441',
                  'sub58949', 'sub60624', 'sub76987', 'sub84403', 'sub86146',
                  'sub90179', 'sub94293']

        # Generate the list of files by session
        anat_anon_files = [
            [(os.path.join('session1', sub, p_anon), fa1, fa1_opts)
                for sub in subs_a]
            + [(os.path.join('session1', sub, p_anon), fb1, fb1_opts)
                for sub in subs_b],
            [(os.path.join('session2', sub, p_anon), fa2, fa2_opts)
                for sub in subs_a]
            + [(os.path.join('session2', sub, p_anon), fb2, fb2_opts)
                for sub in subs_b],
            [(os.path.join('session3', sub, p_anon), fa3, fa3_opts)
                for sub in subs_a]
            + [(os.path.join('session3', sub, p_anon), fb3, fb3_opts)
                for sub in subs_b]]

        anat_skull_files = [
            [(os.path.join('session1', sub, p_skull), fa1, fa1_opts)
                for sub in subs_a]
            + [(os.path.join('session1', sub, p_skull), fb1, fb1_opts)
                for sub in subs_b],
            [(os.path.join('session2', sub, p_skull), fa2, fa2_opts)
                for sub in subs_a]
            + [(os.path.join('session2', sub, p_skull), fb2, fb2_opts)
                for sub in subs_b],
            [(os.path.join('session3', sub, p_skull), fa3, fa3_opts)
                for sub in subs_a]
            + [(os.path.join('session3', sub, p_skull), fb3, fb3_opts)
                for sub in subs_b]]

        func_files = [
            [(os.path.join('session1', sub, p_func), fa1, fa1_opts)
                for sub in subs_a]
            + [(os.path.join('session1', sub, p_func), fb1, fb1_opts)
                for sub in subs_b],
            [(os.path.join('session2', sub, p_func), fa2, fa2_opts)
                for sub in subs_a]
            + [(os.path.join('session2', sub, p_func), fb2, fb2_opts)
                for sub in subs_b],
            [(os.path.join('session3', sub, p_func), fa3, fa3_opts)
                for sub in subs_a]
            + [(os.path.join('session3', sub, p_func), fb3, fb3_opts)
                for sub in subs_b]]

        max_subjects = len(subs_a) + len(subs_b)

        # Check arguments
        if n_subjects is None:
            n_subjects = len(subs_a) + len(subs_b)
        if n_subjects > max_subjects:
            warnings.warn('Warning: there are only %d subjects' % max_subjects)
            n_subjects = 25

        anat_anon = []
        anat_skull = []
        func = []
        session = []
        for i in sessions:
            if not (i in [1, 2, 3]):
                raise ValueError('NYU dataset session id must be in [1, 2, 3]')
            anat_anon += anat_anon_files[i - 1][:n_subjects]
            anat_skull += anat_skull_files[i - 1][:n_subjects]
            func += func_files[i - 1][:n_subjects]
            session += [i] * n_subjects

        anat_anon = self.fetcher.fetch(anat_anon, resume=resume,
                                       force=force, verbose=verbose)
        anat_skull = self.fetcher.fetch(anat_skull, resume=resume,
                                        force=force, verbose=verbose)
        func = self.fetcher.fetch(func, resume=resume,
                                  force=force, verbose=verbose)

        return Bunch(anat_anon=anat_anon, anat_skull=anat_skull, func=func,
                     session=session)


def fetch_nyu_rest(n_subjects=None, sessions=[1], data_dir=None, resume=True,
                   verbose=1):
    return NyuRestDataset(data_dir=data_dir).fetch(n_subjects=n_subjects,
                                                   sessions=sessions,
                                                   resume=resume,
                                                   verbose=verbose)
