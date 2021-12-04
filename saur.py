#!/usr/bin/python3
'''
Easy management of AUR local repository
'''
import sys
import argparse
from xdg.BaseDirectory import (xdg_data_home, xdg_config_home, xdg_cache_home)

from saur import version
from saur import config
from saur import aur

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='saur', description='This is SAUR, the Emperor of AUR/PKGBUILD local repository management.')
    parser.add_argument('--version', action='version', version=f'%(prog)s {version.__version__}', help='print version and exit')
    parser.add_argument('-c','--config', metavar='PATH', type=str, default=xdg_config_home + '/saur/config.ini',
            help='path to config file (default: $XDG_CONFIG_HOME/saur/config.ini)')

    subparsers = parser.add_subparsers(required=True, dest='cmd', title='subcommands')
    parser_createdb = subparsers.add_parser('createdb', help='create a new pacman package database')
    parser_rmpkg = subparsers.add_parser('rmpkg', help='remove package(s) from package database')
    parser_fetch = subparsers.add_parser('fetch', help='fetch packages (this overwrites all changes!)')
    parser_fetch.add_argument('-C', '--clear-cache', action='store_true', help='clear the cache before fetching')
    parser_list = subparsers.add_parser('list', help='print list of packages in CONFIG')
    parser_rebuild = subparsers.add_parser('rebuild', help='rebuild a package (or more) and replace it in the repository')
    parser_rebuild.add_argument(dest='packages', metavar='PACKAGE', nargs='+', help='package(s) to be rebuilt')
    parser_sync = subparsers.add_parser('sync', help='build a package (or more) if it is newer then in the repository')
    parser_sync.add_argument('-x', '--exclude', metavar='PACKAGE', nargs='+', help='package(s) that should not be sync\'d')

    args = parser.parse_args ()

    Config = config.SaurConfig (args.config)
    Config.parse_config ()

    Aur = aur.Aur ()

    if args.cmd == 'sync':
        Aur.sync (Config.config(), args.exclude)
    elif args.cmd == 'rebuild':
        pass
        #run_rebuild (conf, args.packages)
    elif args.cmd == 'list':
        Aur.list (Config.config())
    elif args.cmd == 'fetch':
        Aur.fetch (Config.config(), clearcache=args.clear_cache)
    else:
        print(f'Command `{args.cmd}\' is not implemented!')
        sys.exit(2)
