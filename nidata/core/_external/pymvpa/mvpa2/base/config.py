# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Registry-like monster"""

__docformat__ = 'restructuredtext'

from ConfigParser import SafeConfigParser
import os
from os.path import join as pathjoin


class ConfigManager(SafeConfigParser):
    """Central configuration registry for PyMVPA.

    The purpose of this class is to collect all configurable settings used by
    various parts of PyMVPA. It is fairly simple and does only little more
    than the standard Python ConfigParser. Like ConfigParser it is blind, and in addition,
    looks for special environment variables. Some examples::

        MVPA_VERBOSE=1

    will become::

        [general]
        verbose = 1

    However, `MVPA_VERBOSE_OUTPUT=stdout` becomes::

        [verbose]
        output = stdout

    Any length of variable name as allowed, e.g. MVPA_SEC1_LONG_VARIABLE_NAME=1
    becomes::

        [sec1]
        long variable name = 1


    """

    # things we want to count on to be available
    _DEFAULTS = {'general':
                  {
                    'verbose': '1',
                  }
                }


    def __init__(self, filenames=None):
        """Initialization reads settings from config files and env. variables.

        Parameters
        ----------
        filenames : list of filenames
        """
        SafeConfigParser.__init__(self)

        # store additional config file names
        if not filenames is None:
            self.__cfg_filenames = filenames
        else:
            self.__cfg_filenames = []

        # set critical defaults
        for sec, vars in ConfigManager._DEFAULTS.iteritems():
            self.add_section(sec)
            for key, value in vars.iteritems():
                self.set(sec, key, value)

        # now get the setting
        self.reload()


    def reload(self):
        """Re-read settings from all configured locations.
        """
        # listof filenames to parse (custom plus some standard ones)
        homedir = os.path.expanduser('~')
        user_configfile = pathjoin(homedir, '.pymvpa2.cfg')
        user_configfile_old = pathjoin(homedir, '.pymvpa.cfg')
        # first load user config and then overwrite by local and custom config
        # files.
        filenames = [user_configfile, 'pymvpa2.cfg'] + self.__cfg_filenames

        # Check if config for previous version exists, we need to
        # warn users since they might need to copy it over
        if not os.path.exists(user_configfile) and \
            os.path.exists(user_configfile_old):
            # but we can't use our 'warning' since it would not be
            # defined yet and import here would be circular
            # so use stock Python one
            from warnings import warn
            warn("You seems to have a configuration file %s for previous "
                 "version of PyMVPA but lacking configuration for PyMVPA2. "
                 "Consider copying it into %s"
                 % (user_configfile_old, user_configfile))

        # read local and user-specific config
        files = self.read(filenames)

        # no look for variables in the environment
        for var in [v for v in os.environ.keys() if v.startswith('MVPA_')]:
            # strip leading 'MVPA_' and lower case entries
            svar = var[5:].lower()

            # section is next element in name (or 'general' if simple name)
            if not svar.count('_'):
                sec = 'general'
            else:
                cut = svar.find('_')
                sec = svar[:cut]
                svar = svar[cut + 1:].replace('_', ' ')

            # check if section is already known and add it if not
            if not self.has_section(sec):
                self.add_section(sec)

            # set value
            self.set(sec, svar, os.environ[var])


    def __repr__(self):
        """Generate INI file content with current configuration.
        """
        # make adaptor to use str as file-like (needed for ConfigParser.write()
        class file2str(object):
            def __init__(self):
                self.__s = ''
            def write(self, val):
                self.__s += val
            def str(self):
                return self.__s

        r = file2str()
        self.write(r)

        return r.str()


    def save(self, filename):
        """Write current configuration to a file.
        """
        f = open(filename, 'w')
        self.write(f)
        f.close()


    def get(self, section, option, default=None, **kwargs):
        """Wrapper around SafeConfigParser.get() with a custom default value.

        This method simply wraps the base class method, but adds a `default`
        keyword argument. The value of `default` is returned whenever the
        config parser does not have the requested option and/or section.
        """
        if not self.has_option(section, option):
            return default

        try:
            return SafeConfigParser.get(self, section, option, **kwargs)
        except ValueError, e:
            # provide somewhat descriptive error
            raise ValueError, \
                  "Failed to obtain value from configuration for %s.%s. " \
                  "Original exception was: %s" % (section, option, e)


    def getboolean(self, section, option, default=None):
        """Wrapper around SafeConfigParser.getboolean() with a custom default.

        This method simply wraps the base class method, but adds a `default`
        keyword argument. The value of `default` is returned whenever the
        config parser does not have the requested option and/or section.
        """
        if not self.has_option(section, option):
            if isinstance(default, bool):
                return default
            else:
                # compatibility layer for py3 version of ConfigParser
                if hasattr(self, '_boolean_states'):
                    boolean_states = self._boolean_states
                else:
                    boolean_states = self.BOOLEAN_STATES
                if default.lower() not in boolean_states:
                    raise ValueError, 'Not a boolean: %s' % default
                return boolean_states[default.lower()]

        return SafeConfigParser.getboolean(self, section, option)


    ##REF: Name was automagically refactored
    def get_as_dtype(self, section, option, dtype, default=None):
        """Convenience method to query options with a custom default and type

        This method simply wraps the base class method, but adds a `default`
        keyword argument. The value of `default` is returned whenever the
        config parser does not have the requested option and/or section.

        In addition, the returned value is converted into the specified `dtype`.
        """
        if not self.has_option(section, option):
            return default
        try:
            return SafeConfigParser._get(self, section, dtype, option)
        except ValueError, e:
            # provide somewhat descriptive error
            raise ValueError, \
                  "Failed to obtain value from configuration for %s.%s. " \
                  "Original exception was: %s" % (section, option, e)
