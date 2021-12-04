'''
module handles config
'''
import os
import sys
import configparser
from xdg.BaseDirectory import (xdg_data_home, xdg_config_home, xdg_cache_home)

class SaurConfigError (Exception):
    '''Exception for when an error occurs within the SaurConfig class.'''
    def __init__ (self, message, errorcode=None):
        super ().__init__ (message)
        if errorcode:
            self.errors = errorcode

class SaurConfig ():
    def __init__ (self, conf_file):
        if not os.path.exists (conf_file):
            raise SaurConfigError (f'No config file at {conf_file}!')

        self.file = conf_file
        self.defconf = { 'verbose': False,
                 'cachedir': xdg_cache_home + '/saur',
                 'datadir': xdg_data_home + '/saur',
                 'dbroot': None,
                 'dbname': None,
                 'gpgkey': None,
                 'flags':
                 { 'def': [],
                   'sync': ["-n", "-s", "-r", "--clean"],
                   'rebuild': ["-n", "--noview", "--continue", "--rebuild"] },
                 'packages': None,
                 'bpackages': None }

    def config (self):
        return self.defconf

    def parse_config (self):
        with open (self.file, 'r', encoding='ascii') as fp:
            config = configparser.ConfigParser (allow_no_value=True)
            config.read_file (fp)

            if 'settings' in config:
                print ('Reading in settings... ', end='')
                self.defconf.update (config['settings'])
                for k, v in self.defconf.items():
                    if v in ('false', 'False'):
                        self.defconf[k] = False
                    if v in ('true', 'True'):
                        self.defconf[k] = True
                print ('done')

            if 'packages' not in config or not config['packages']:
                raise SaurConfigError ('The config file has no packages listed!')
            else:
                self.defconf['packages'] = dict(config.items('packages', raw=True))
                self.defconf['bpackages'] = {}

            if self.defconf['dbroot']:
                self.defconf['flags']['def'].append(f'--root={self.defconf["dbroot"]}')
            if self.defconf['dbname']:
                self.defconf['flags']['def'].append('-d')
                self.defconf['flags']['def'].append(self.defconf['dbname'])
            if self.defconf['gpgkey']:
                self.defconf['flags']['def'].append('--sign')

            if self.defconf['verbose']:
                print (self.defconf)
