#!/usr/bin/env python
#
# Setup script for Review Board.
#
# A big thanks to Django project for some of the fixes used in here for
# MacOS X and data files installation.

from __future__ import print_function, unicode_literals

import json
import os
import subprocess
import sys
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import Command

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

from reviewboard import get_package_version, VERSION
from reviewboard.dependencies import (PYTHON_2_MIN_VERSION,
                                      PYTHON_2_MIN_VERSION_STR,
                                      PYTHON_3_MIN_VERSION,
                                      PYTHON_3_MIN_VERSION_STR,
                                      build_dependency_list,
                                      package_dependencies,
                                      package_only_dependencies)


is_packaging = ('sdist' in sys.argv or
                'bdist_egg' in sys.argv or
                'bdist_wheel' in sys.argv or
                'install' in sys.argv)


# Make sure this is a version of Python we are compatible with. This should
# prevent people on older versions from unintentionally trying to install
# the source tarball, and failing.
pyver = sys.version_info[:2]

if pyver < PYTHON_2_MIN_VERSION or (3, 0) <= pyver < PYTHON_3_MIN_VERSION:
    sys.stderr.write(
        'Review Board %s is incompatible with your version of Python.\n'
        'Please install Review Board 3.0.x or upgrade to either Python %s or '
        '%s+.\n'
        % (get_package_version(), PYTHON_2_MIN_VERSION_STR,
           PYTHON_3_MIN_VERSION_STR))
    sys.exit(1)


# NOTE: When updating, make sure you update the classifiers below.
SUPPORTED_PYVERS = ['2.7', '3.6', '3.7', '3.8', '3.9']


if '--all-pyvers' in sys.argv:
    new_argv = sys.argv[1:]
    new_argv.remove('--all-pyvers')

    for pyver in SUPPORTED_PYVERS:
        result = os.system(subprocess.list2cmdline(
            ['python%s' % pyver, __file__] + new_argv))

        if result != 0:
            sys.exit(result)

    sys.exit(0)

if '--pyvers' in sys.argv:
    i = sys.argv.index('--pyvers')
    pyvers = sys.argv[i + 1].split()

    new_argv = sys.argv[1:]
    del new_argv[i - 1:i + 1]

    for pyver in pyvers:
        if pyver not in SUPPORTED_PYVERS:
            sys.stderr.write('Python version %s is not in SUPPORTED_PYVERS'
                             % pyver)
            sys.exit(1)

        result = os.system(subprocess.list2cmdline(
            ['python%s' % pyver, __file__] + new_argv))

        if result != 0:
            sys.exit(result)

    sys.exit(0)


# Make sure we're actually in the directory containing setup.py.
root_dir = os.path.dirname(__file__)

if root_dir != '':
    os.chdir(root_dir)


# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


if is_packaging:
    # If we're packaging, include the package-only dependencies.
    package_dependencies = package_dependencies.copy()
    package_dependencies.update(package_only_dependencies)


class BuildEggInfoCommand(egg_info):
    """Build the egg information for the package.

    If this is called when building a distribution (source, egg, or wheel),
    or when installing the package from source, this will kick off tasks for
    building static media and string localization files.
    """

    def run(self):
        """Build the egg information."""
        if is_packaging:
            self.run_command('build_media')
            self.run_command('build_i18n')

        egg_info.run(self)


class DevelopCommand(develop):
    """Installs Review Board in developer mode.

    This will install all standard and development dependencies (using Python
    wheels and node.js packages from npm) and add the source tree to the
    Python module search path. That includes updating the versions of pip
    and setuptools on the system.

    To speed up subsequent runs, callers can pass ``--no-npm`` to prevent
    installing node.js packages.
    """

    user_options = develop.user_options + [
        (str('no-npm'), None, "Don't install packages from npm"),
        (str('use-npm-cache'), None, 'Use npm-cache to install packages'),
        (str('with-doc-deps'), None,
         'Install documentation-related dependencies'),
    ]

    boolean_options = develop.boolean_options + [
        str('no-npm'),
        str('use-npm-cache'),
        str('with-doc-deps'),
    ]

    def initialize_options(self):
        """Initialize options for the command."""
        develop.initialize_options(self)

        self.no_npm = None
        self.with_doc_deps = None
        self.use_npm_cache = None

    def install_for_development(self):
        """Install the package for development.

        This takes care of the work of installing all dependencies.
        """
        if self.no_deps:
            # In this case, we don't want to install any of the dependencies
            # below. However, it's really unlikely that a user is going to
            # want to pass --no-deps.
            #
            # Instead, what this really does is give us a way to know we've
            # been called by `pip install -e .`. That will call us with
            # --no-deps, as it's going to actually handle all dependency
            # installation, rather than having easy_install do it.
            develop.install_for_development(self)
            return

        # Install the dependencies using pip instead of easy_install. This
        # will use wheels instead of legacy eggs.
        self._run_pip(['install', '--no-build-isolation', '-e', '.'])
        self._run_pip(['install', '--no-build-isolation',
                       '-r', 'dev-requirements.txt'])

        if self.with_doc_deps:
            self._run_pip(['install', '--no-build-isolation',
                           '-r', 'doc-requirements.txt'])

        if not self.no_npm:
            # Install node.js dependencies, needed for packaging.
            if self.use_npm_cache:
                self.distribution.command_options['install_node_deps'] = {
                    'use_npm_cache': ('install_node_deps', 1),
                }

            self.run_command('install_node_deps')

    def _run_pip(self, args):
        """Run pip.

        Args:
            args (list):
                Arguments to pass to :command:`pip`.

        Raises:
            RuntimeError:
                The :command:`pip` command returned a non-zero exit code.
        """
        cmd = subprocess.list2cmdline([sys.executable, '-m', 'pip'] + args)
        ret = os.system(cmd)

        if ret != 0:
            raise RuntimeError('Failed to run `%s`' % cmd)


class BuildMediaCommand(Command):
    """Builds static media files for the package.

    This requires first having the node.js dependencies installed.
    """

    user_options = []

    def initialize_options(self):
        """Initialize options for the command.

        This is required, but does not actually do anything.
        """
        pass

    def finalize_options(self):
        """Finalize options for the command.

        This is required, but does not actually do anything.
        """
        pass

    def run(self):
        """Runs the commands to build the static media files.

        Raises:
            RuntimeError:
                Static media failed to build.
        """
        retcode = subprocess.call([
            sys.executable, 'contrib/internal/build-media.py'])

        if retcode != 0:
            raise RuntimeError('Failed to build media files')


class BuildI18nCommand(Command):
    """Builds string localization files."""

    description = 'Compile message catalogs to .mo'
    user_options = []

    def initialize_options(self):
        """Initialize options for the command.

        This is required, but does not actually do anything.
        """
        pass

    def finalize_options(self):
        """Finalize options for the command.

        This is required, but does not actually do anything.
        """
        pass

    def run(self):
        """Runs the commands to build the string localization files.

        Raises:
            RuntimeError:
                Localization files failed to build.
        """
        retcode = subprocess.call([
            sys.executable, 'contrib/internal/build-i18n.py'])

        if retcode != 0:
            raise RuntimeError('Failed to build i18n files')


class ListNodeDependenciesCommand(Command):
    """"Write all node.js dependencies to standard output."""

    description = 'Generate a package.json that lists node.js dependencies'

    user_options = [
        (str('to-stdout'), None,
         'Write to standard output instead of a package.json file.')
    ]

    boolean_options = [str('to-stdout')]

    def initialize_options(self):
        """Set the command's option defaults."""
        self.to_stdout = False

    def finalize_options(self):
        """Post-process command options.

        This method intentionally left blank.
        """
        pass

    def run(self):
        """Run the command."""
        if self.to_stdout:
            self._write_deps(sys.stdout)
        else:
            with open('package.json', 'w') as f:
                self._write_deps(f)

    def _write_deps(self, f):
        """Write the packaage.json to the given file handle.

        Args:
            f (file):
                The file handle to write to.
        """
        from djblets.dependencies import npm_dependencies

        f.write(json.dumps(
            {
                'name': 'reviewboard',
                'private': 'true',
                'devDependencies': {},
                'dependencies': npm_dependencies,
            },
            indent=2))
        f.write('\n')


class InstallNodeDependenciesCommand(Command):
    """Install all node.js dependencies from npm.

    If ``--use-npm-cache`` is passed, this will use :command:`npm-cache`
    to install the packages, which is best for Continuous Integration setups.
    Otherwise, :command:`npm` is used.
    """

    description = \
        'Install the node packages required for building static media.'

    user_options = [
        (str('use-npm-cache'), None, 'Use npm-cache to install packages'),
    ]

    boolean_options = [str('use-npm-cache')]

    def initialize_options(self):
        """Initialize options for the command."""
        self.use_npm_cache = None

    def finalize_options(self):
        """Finalize options for the command.

        This is required, but does not actually do anything.
        """
        pass

    def run(self):
        """Run the commands to install packages from npm.

        Raises:
            RuntimeError:
                There was an error finding or invoking the package manager.
        """
        if self.use_npm_cache:
            npm_command = 'npm-cache'
        else:
            npm_command = 'npm'

        try:
            subprocess.check_call([npm_command, '--version'])
        except subprocess.CalledProcessError:
            raise RuntimeError(
                'Unable to locate %s in the path, which is needed to '
                'install dependencies required to build this package.'
                % npm_command)

        # By this point, dependencies should be installed for us. We're also
        # using the same exact dependencies as Djblets, so no need to
        # duplicate that list.
        self.run_command('list_node_deps')

        print('Installing node.js modules...')
        result = os.system('%s install' % npm_command)

        os.unlink('package.json')

        if result != 0:
            raise RuntimeError(
                'One or more node.js modules could not be installed.')


def build_entrypoints(prefix, entrypoints):
    """Build and return a list of entrypoints from a module prefix and list.

    This is a utility function to help with constructing entrypoints to pass
    to :py:func:`~setuptools.setup`. It takes a module prefix and a condensed
    list of tuples of entrypoint names and relative module/class paths.

    Args:
        prefix (unicode):
            The prefix for each module path.

        entrypoints (list of tuple):
            A list of tuples of entries for the entrypoints. Each tuple
            contains an entrypoint name and a relative path to append to the
            prefix.

    Returns:
        list of unicode:
        A list of entrypoint items.
    """
    result = []

    for entrypoint_id, rel_class_name in entrypoints:
        if ':' in rel_class_name:
            sep = '.'
        else:
            sep = ':'

        result.append('%s = %s%s%s' % (entrypoint_id, prefix, sep,
                                       rel_class_name))

    return result


PACKAGE_NAME = 'ReviewBoard'


with open('README.rst', 'r') as fp:
    long_description = fp.read()


setup(
    name=PACKAGE_NAME,
    version=get_package_version(),
    license='MIT',
    description=(
        'Review Board, a fully-featured web-based code and document '
        'review tool made with love <3'
    ),
    long_description=long_description,
    author='Beanbag, Inc.',
    author_email='reviewboard@googlegroups.com',
    url='https://www.reviewboard.org/',
    download_url=('https://downloads.reviewboard.org/releases/%s/%s.%s/'
                  % (PACKAGE_NAME, VERSION[0], VERSION[1])),
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': build_entrypoints(
            'reviewboard.cmdline',
            [
                ('rb-site', 'rbsite:main'),
                ('rbext', 'rbext:main'),
                ('rbssh', 'rbssh:main'),
            ]
        ),
        'reviewboard.hosting_services': build_entrypoints(
            'reviewboard.hostingsvcs',
            [
                ('assembla', 'assembla:Assembla'),
                ('beanstalk', 'beanstalk:Beanstalk'),
                ('bitbucket', 'bitbucket:Bitbucket'),
                ('bugzilla', 'bugzilla:Bugzilla'),
                ('codebasehq', 'codebasehq:CodebaseHQ'),
                ('fedorahosted', 'fedorahosted:FedoraHosted'),
                ('fogbugz', 'fogbugz:FogBugz'),
                ('gerrit', 'gerrit:Gerrit'),
                ('github', 'github:GitHub'),
                ('gitlab', 'gitlab:GitLab'),
                ('gitorious', 'gitorious:Gitorious'),
                ('googlecode', 'googlecode:GoogleCode'),
                ('jira', 'jira:JIRA'),
                ('kiln', 'kiln:Kiln'),
                ('rbgateway', 'rbgateway:ReviewBoardGateway'),
                ('redmine', 'redmine:Redmine'),
                ('sourceforge', 'sourceforge:SourceForge'),
                ('splat', 'splat:Splat'),
                ('trac', 'trac:Trac'),
                ('unfuddle', 'unfuddle:Unfuddle'),
                ('versionone', 'versionone:VersionOne'),
            ]
        ),
        'reviewboard.scmtools': build_entrypoints(
            'reviewboard.scmtools',
            [
                ('bzr', 'bzr:BZRTool'),
                ('clearcase', 'clearcase:ClearCaseTool'),
                ('cvs', 'cvs:CVSTool'),
                ('git', 'git:GitTool'),
                ('hg', 'hg:HgTool'),
                ('perforce', 'perforce:PerforceTool'),
                ('plastic', 'plastic:PlasticTool'),
                ('svn', 'svn:SVNTool'),
            ]
        ),
        'reviewboard.auth_backends': build_entrypoints(
            'reviewboard.accounts.backends',
            [
                ('ad', 'ad:ActiveDirectoryBackend'),
                ('ldap', 'ldap:LDAPBackend'),
                ('nis', 'nis:NISBackend'),
                ('x509', 'x509:X509Backend'),
                ('digest', 'http_digest:HTTPDigestBackend'),
            ]
        ),
    },
    install_requires=build_dependency_list(package_dependencies),
    extras_require={
        'ldap': [
            'python-ldap>=3.3.1,<3.999; python_version < "3"',
            'python-ldap>=3.3.1; python_version >= "3"',
        ],
        'mercurial': ['mercurial'],
        'mysql': [
            'mysqlclient>=1.4,<=1.4.999; python_version < "3"',
            'mysqlclient>=1.4; python_version >= "3"',
        ],
        'p4': ['p4python'],

        # psycopg2-binary 2.9 breaks Django < 2.2. For now, we must
        # cap it. See https://github.com/psycopg/psycopg2/issues/1293
        'postgres': ['psycopg2-binary<2.9'],

        's3': ['django-storages>=1.8,<1.9'],
        'subvertpy': ['subvertpy'],
        'swift': ['django-storage-swift'],
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'develop': DevelopCommand,
        'egg_info': BuildEggInfoCommand,
        'build_media': BuildMediaCommand,
        'build_i18n': BuildI18nCommand,
        'install_node_deps': InstallNodeDependenciesCommand,
        'list_node_deps': ListNodeDependenciesCommand,
    },
    python_requires=','.join([
        '>=2.7',
        '!=3.0.*',
        '!=3.1.*',
        '!=3.2.*',
        '!=3.3.*',
        '!=3.4.*',
        '!=3.5.*',
    ]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
