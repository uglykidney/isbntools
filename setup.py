# -*- coding: utf-8 -*-

# isbntools - tools for extracting, cleaning and transforming ISBNs
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import pkg_resources
from setuptools import setup
from isbntools import __version__


# CHECK SUPPORT

SUPPORTED = ((2, 6), (2, 7), (3, 3), (3, 4))
if tuple(int(x) for x in sys.version[:3].split('.')) not in SUPPORTED:
    raise Exception('isbntools %s  requires Python 2.6+ or 3.3+.' %
                    __version__)


# ENV

ARGVS = sys.argv
FIRSTRUN = 'egg_info' in ARGVS
PIP = '-c' in ARGVS
INSTALL = any((m in ARGVS for m in ('install', 'develop'))) or PIP
WINDOWS = os.name == 'nt'
VIRTUAL = True if hasattr(sys, 'real_prefix') else False
SECONDRUN = INSTALL and not FIRSTRUN


# DEFS

CONFDIR = '.isbntools' if not WINDOWS else 'isbntools'
CONFFILE = 'isbntools.conf'
CONFRES = pkg_resources.resource_filename('isbntools', CONFFILE)


# HELPERS

def uxchown(fp):
    from pwd import getpwnam, getpwuid
    from grp import getgrnam, getgrgid
    uid = getpwnam(os.getenv("SUDO_USER", getpwuid(os.getuid()).pw_name)).pw_uid
    gid = getgrnam(os.getenv("SUDO_USER", getgrgid(os.getgid()).gr_name)).gr_gid
    os.chown(fp, uid, gid)


def data_path():
    if VIRTUAL:
        installpath = ''
    else:
        user = '~%s' % os.getenv("SUDO_USER", '')
        homepath = os.path.expanduser(user) if not WINDOWS else os.getenv('APPDATA')
        installpath = os.path.join(homepath, CONFDIR)
        if not os.path.exists(installpath) and INSTALL:
            print('making data dir %s' % installpath)
            os.mkdir(installpath)
            uxchown(installpath)
    return installpath


# SET VARIABLES

scripts = ['bin/isbn_validate',
           'bin/to_isbn10',
           'bin/to_isbn13',
           'bin/isbn_mask',
           'bin/isbn_info',
           'bin/isbn_meta',
           'bin/isbntools',
           'bin/isbn_stdin_validate',
           'bin/isbn_from_words',
           'bin/isbn_editions',
           'bin/isbn_goom',
           'bin/isbn_doi',
           'bin/isbn_EAN13',
           'bin/isbn_conf',
           'bin/isbn_ren',
           ]


DATAPATH = data_path()

data_files = [
    (DATAPATH, [CONFRES])
]


# PRE-SETUP

if SECONDRUN and WINDOWS:
    # add expension to scripts
    scripts = [s + '.py' for s in scripts]
    print('adding file extensions...')
    for s in scripts:
        os.rename(s.split('.')[0], s)


# SETUP

setup(
    name='isbntools',
    version=__version__,
    author='xlcnd',
    author_email='xlcnd@outlook.com',
    url='https://github.com/xlcnd/isbntools',
    download_url='https://github.com/xlcnd/isbntools/archive/master.zip',
    packages=['isbntools',
              'isbntools/dev',
              'isbntools/data',
              'isbntools/contrib',
              'isbntools/contrib/plugins',
              'isbntools/contrib/modules',
              'isbntools/contrib/modules/goom',
              'isbntools/contrib/modules/gwords'
              ],
    scripts=scripts,
    data_files=data_files,
    license='LGPL v3',
    description='Extract, clean, transform, hyphenate and metadata for ISBNs (International Standard Book Number).',
    long_description=open('README.rst').read(),
    keywords='ISBN, validate, transform, hyphenate, metadata, World Catalogue, Google Books, Open Library, isbndb.com, BibTeX, EndNote, RefWorks, MSWord, BibJSON, ISBN-A, doi',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)


# POS-SETUP

if not VIRTUAL and not WINDOWS and SECONDRUN:
    conffile = os.path.join(DATAPATH, CONFFILE)
    if not os.path.exists(conffile):
        print("Warning: file %s doesn't exist! Use 'isbn_conf make'" % conffile)
        sys.exit()
    try:
        uxchown(conffile)
        print('changing mode of %s to 666' % conffile)
    except:
        print('Warning: permissions not set for file %s' % conffile)
