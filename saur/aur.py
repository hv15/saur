'''
This modules wraps around the `aur` shell script (and subcommands)
created by Alad Wenter (https://github.com/AladW/aurutils).
'''

from .version import __version__

import subprocess

class Aur:
    def __init__ (self, config, aur_path = None):
        '''
        Initialise the AUR object, which provides an interface to interact
        with aurutils commands.
        '''
        if not self.__check_aurutils_exists (aur_path):
            raise RuntimeError ('Unable to find the `aur` binary, do you have aurutils installed?')

        self.config = config
    def fetch (self, packages, recursive=False, force=False):
        pass

    def sync (self, packages, ):
        pass

    def __check_aurutils_exists (self, path = None):
        '''
        Indicate if the `aur` script is available via PATH
        '''
        from shutil import which
        binary = path if path else which ('aur')
        if binary:
            res = subprocess.run ([binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return res.returncode == 1
        else:
            return False
