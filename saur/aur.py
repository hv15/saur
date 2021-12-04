'''
This modules wraps around the `aur` shell script (and subcommands)
created by Alad Wenter (https://github.com/AladW/aurutils).
'''
import os
import sys
import subprocess
import git
from shutil import which

from .version import __version__

class Aur:
    def __init__ (self, aur_path = None):
        '''
        Initialise the AUR object, which provides an interface to interact
        with aurutils commands.
        '''
        binary = self.__get_binary_path ('aur', aur_path)
        if not binary:
            raise RuntimeError ('Unable to find the \'aur` binary, do you have aurutils installed?')
        else:
            self.aur_binary = binary

        binary = self.__get_binary_path ('patch')
        if not binary:
            raise RuntimeError ('Unable to find the \'patch` binary, do you have patch installed?')
        else:
            self.patch_binary = binary

    def list (self, conf):
        wid = len(max (conf['packages'], key=len))+1
        print ('\n  {:<{width}} |  Action'.format('Package', width=wid))
        print (' ', ('{0}'*(wid-1)).format('-'), ' +  ------')
        for p, c in conf['packages'].items():
            print ('  {:<{width}} :  {}'.format(p, 'default' if c is None else 'patch', width=wid))

    def __resolveb (self, conf):
        print ('Resloving package base names... ', end='')
        for pkg in conf['packages'].keys():
            bname = self.__basepkg (pkg)
            if pkg != bname:
                conf['bpackages'] = {pkg: bname}
        print ('done')

    def fetch (self, conf, clearcache=False, recursive=False, force=False):
        if not os.path.isdir (conf['cachedir']):
            print (f"Unable to find {conf['cachedir']}, creating it...")
            os.makedirs (conf['cachedir'])

        cmd = [self.aur_binary, "fetch", "-r", "--sync=reset"]

        for p, v in conf['packages'].items():
            # determine base names
            b = self.__basepkg (p)
            if b != p:
                conf['bpackages'][p] = b

            print (f"Fetching packge '{p}'... ", end='')
            if clearcache:
                print ("[clearing cache]... ", end='')
                path = os.path.join(conf['cachedir'], self.__in_packages (conf, p))
                if os.path.exists (path):
                    # we intentionally do a clean to remove all left-overs from previous build
                    repo = git.Repo (path)
                    repo.git.clean('-xdf')
            self.__cmd (cmd + [p], cwd=conf['cachedir'])
            print ('done')

    def __in_packages (self, conf, p):
        if p in conf['bpackages']:
            return conf['bpackages'][p]
        elif p in conf['packages']:
            return p
        else:
            return None

    def rebuild (self, packages, conf):
        rebuild_list = []
        for p in packages:
            # we want to the base package name
            bp = self.__in_packages (conf, p)
            if not bp:
                print (f'Rebuilding new packages is not supported: {p}')
            elif not os.path.exists (conf['cachedir'] + '/' + bp):
                print (f'Package {p} was never fetched!')
            else:
                rebuild_list.append(p)

        os.environ['AURDEST'] = conf['cachedir']
        # if we are signing, we need to set the default key to use
        if conf['gpgkey']:
            os.environ['GPGKEY'] = conf['gpgkey']
        self.__cmd (["aur", "sync"] + conf['flags']['rebuild'] + conf['flags']['def'] + rebuild_list, inline=True)

    def __apply_custom (self, conf):
        if not os.path.isdir (conf['datadir']):
            print (f"Unable to find {conf['datadir']}, creating it...")
            os.makedirs (conf['datadir'])

        for p, v in conf['packages'].items ():
            if v is not None:
                if p in conf['bpackages']:
                    bname = conf['bpackages'][p]
                else:
                    bname = p

                if os.path.isdir (conf['datadir'] + '/' + bname):
                    print (f'Customising `{bname}\':')
                    for f in os.listdir (conf['datadir'] + '/' + bname):
                        if f.endswith (".patch"):
                            self.__cmd ([self.patch_binary, "-d", conf['cachedir'] + '/' + bname, "-p1", "-i", conf['datadir'] + '/' + bname + '/' + f])
                            print (f'  Applied patch `{f}\'')
                else:
                    print (f'Unable to find patches for `{bname}\'!')
                    sys.exit (4)

    def sync (self, conf, exclude):
        if exclude:
            # remove members in exclude from package list
            p = set(conf['packages'])
            pp = p.difference (set (exclude))
            conf['packages'] = list(pp)

        # we fetch the packages
        self.fetch (conf)

        # we apply any customisations
        self.__apply_custom (conf)

        # if we are signing, we need to set the default key to use
        if conf['gpgkey']:
            os.environ['GPGKEY'] = conf['gpgkey']

        for p, v in conf['packages'].items ():
            bname = self.__in_packages (conf, p)
            print (f"Sync package '{bname}'...", end='')

            if os.path.isdir (conf['cachedir'] + '/' + bname):
                self.__cmd ([self.aur_binary, "build"] + conf['flags']['sync'] + conf['flags']['def'], cwd=conf['cachedir'] + '/' + bname, inline=True)
                print ('[built]', end='')
            else:
                print (f'Unable to find directory for `{bname}\'!')
                sys.exit (4)
            print ("Done")

    def __basepkg (self, package):
        '''
        Determine if package is part of a larger package base.
        '''
        ret = self.__cmd ([self.aur_binary, "depends", "-b", package])
        # convert from binary to standard encoding
        return ret.stdout.decode('ascii').strip()

    def __get_binary_path (self, name, path = None):
        '''
        Indicate if the name binary is available via PATH
        '''
        binary = path if path else which (name)
        if binary:
            try:
                subprocess.run ([binary, '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                binary = None
        return binary

    def __cmd (self, cmd, inline=False, cwd=None):
        ret = None
        args = {}
        if inline:
            args['stdout'] = sys.stdout
            args['stderr'] = sys.stderr
        else:
            args['capture_output'] = True

        try:
            ret = subprocess.run (cmd, cwd=cwd, check=True, **args)
        except subprocess.CalledProcessError as e:
            print(f'\nCommand `{" ".join(cmd)}\' failed with return {e.returncode}!')
            if not inline:
                print(' ', e.stderr.decode())
            sys.exit(e.returncode)
        return ret
