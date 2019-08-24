#!/usr/bin/env python3

import configparser
import argparse
import os
import sys
import subprocess
import git
from xdg.BaseDirectory import (xdg_data_home, xdg_config_home, xdg_cache_home)

# global constants
VERSION='1.0.0'

def parse_config (conf_file, conf):
    if not os.path.exists (conf_file):
        print (f'No config file at {conf_file}!')
        sys.exit (3)
    else:
        with open (conf_file, 'r') as fp:
            config = configparser.ConfigParser (allow_no_value=True)
            config.read_file (fp)

            if 'settings' in config:
                print ('Reading in settings... ', end='')
                conf.update (config['settings'])
                for k, v in conf.items():
                    if v == 'false' or v == 'False':
                        conf[k] = False
                    if v == 'true' or v == 'True':
                        conf[k] = True
                print ('done')

            if 'packages' not in config or not config['packages']:
                print ('The config file has no packages listed!')
                sys.exit (1)
            else:
                conf['packages'] = dict(config.items('packages', raw=True))
                conf['bpackages'] = dict()
                print ('Resloving package base names... ', end='')
                for p in conf['packages'].keys():
                    get_basepkg (p, conf)
                print ('done')

            if conf['dbroot']:
                conf['flags']['def'].append('--root=%s' % (conf['dbroot']))
            if conf['dbname']:
                conf['flags']['def'].append('-d')
                conf['flags']['def'].append(conf['dbname'])
            if conf['gpgkey']:
                conf['flags']['def'].append('--sign')

            if conf['verbose']:
                print (conf)

def cmd (cmd, inline=False, cwd=None):
    ret = None
    args = dict()
    if inline:
        args['stdout'] = sys.stdout
        args['stderr'] = sys.stderr
    else:
        args['capture_output'] = True

    try:
        ret = subprocess.run (cmd, cwd=cwd, check=True, **args)
    except subprocess.CalledProcessError as e:
        print(f'\nBinary `{cmd[0]}\' failed with return %d!' % (e.returncode))
        print(e.stderr)
        sys.exit(e.returncode)
    return ret

def get_basepkg (pkg, conf):
    ret = cmd (["aur", "depends", "-b", pkg])
    # convert from binary to standard encoding
    bname = ret.stdout.decode('ascii').strip()
    if pkg != bname:
        conf['bpackages'][pkg] = bname

def apply_custom (conf):
    if not os.path.isdir (conf['datadir']):
        print (f"Unable to find {conf['datadir']}, creating it...")
        os.makedirs (conf['datadir'])

    for p, v in conf['packages'].items ():
        if v != None:
            if p in conf['bpackages']:
                bname = conf['bpackages'][p]
            else:
                bname = p

            if os.path.isdir (conf['datadir'] + '/' + bname):
                print (f'Customising `{bname}\':')
                for f in os.listdir (conf['datadir'] + '/' + bname):
                    if f.endswith (".patch"):
                        cmd (["patch", "-d", conf['cachedir'] + '/' + bname, "-p1", "-i", conf['datadir'] + '/' + bname + '/' + f])
                        print (f'  Applied patch `{f}\'')
            else:
                print (f'Unable to find patches for `{bname}\'!')
                sys.exit (4)

def run_fetch (conf):
    if not os.path.isdir (conf['cachedir']):
        print (f"Unable to find {conf['cachedir']}, creating it...")
        os.makedirs (conf['cachedir'])

    cmd = ["aur", "fetch", "-r"]

    try:
        print ('Fetching packges... ', end='')
        for p, v in conf['packages'].items ():
            if os.path.exists (conf['cachedir'] + '/' + p):
                # we intentionally do a hard reset as aur-fetch
                # would otherwise try to replay and changes. We
                # don't want this as it would conflict with applying
                # patches, especially if they are new.
                repo = git.Repo (conf['cachedir'] + '/' + p)
                repo.git.reset('--hard')
            ret = subprocess.run (cmd + [p], cwd=conf['cachedir'], check=True, capture_output=True)
        print ('done')
    except subprocess.CalledProcessError as e:
        print('\naur-fetch failed with return %d!' % (e.returncode))
        print(e.stderr)
        sys.exit(e.returncode)

def run_sync (conf):
    # we fetch the packages
    run_fetch (conf)

    # we apply any customisations
    apply_custom (conf)

    # we now build and add to db
    os.environ['AURDEST'] = conf['cachedir']
    # if we are signing, we need to set the default key to use
    if conf['gpgkey']:
        os.environ['GPGKEY'] = conf['gpgkey']
    ret = cmd (["aur", "sync"] + conf['flags']['sync'] + conf['flags']['def'] + list(conf['packages'].keys()), inline=True)

def run_list (conf):
    print ('  Package                 Action')
    print ('  -------------------  |  ------')
    for p, c in conf['packages'].items():
        if c is None:
            c = 'default'
        else:
            c = 'patch'
        print (f'  {p:<20} |  {c}')

if __name__ == '__main__':

    # global configuration
    conf = { 'verbose': False,
             'cachedir': xdg_cache_home + '/saur',
             'datadir': xdg_data_home + '/saur',
             'dbroot': None,
             'dbname': None,
             'gpgkey': None,
             'flags':
             { 'def': [],
               'sync': ["-n", "--noview", "--continue"] },
             'packages': None,
             'bpackages': None }

    parser = argparse.ArgumentParser(prog='saur', description='This is SAUR, the Emperor of AUR/PKGBUILD local repository management.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}', help='print version and exit')
    parser.add_argument('-c','--config', metavar='PATH', type=str, default=xdg_config_home + '/saur/config.ini',
            help='path to config file (default: $XDG_CONFIG_HOME/saur/config.ini)')

    subparsers = parser.add_subparsers(required=True, dest='cmd', title='subcommands')
    parser_fetch = subparsers.add_parser('fetch', help='fetch packages (this overwrites all changes!)')
    parser_list = subparsers.add_parser('list', help='print list of packages in CONFIG')
    parser_sync = subparsers.add_parser('sync', help='build a package (or more) if it is newer then in the repository')

    args = parser.parse_args ()
    parse_config (args.config, conf)

    if args.cmd == 'sync':
        run_sync (conf)
    elif args.cmd == 'list':
        run_list (conf)
    elif args.cmd == 'fetch':
        run_fetch (conf)
    else:
        print(f'Command `{args.cmd}\' is not implemented!')
        sys.exit(2)
