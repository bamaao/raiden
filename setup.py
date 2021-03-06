#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from setuptools import Command
from setuptools.command.test import test as TestCommand
from setuptools.command.build_py import build_py


class BuildPyCommand(build_py):

    def run(self):
        self.run_command('compile_contracts')
        # ensure smoketest_config.json is generated
        from raiden.tests.utils.smoketest import load_or_create_smoketest_config
        load_or_create_smoketest_config()
        build_py.run(self)


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


class CompileContracts(Command):
    description = "compile contracts to json"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.environ['STORE_PRECOMPILED'] = 'yes'
        from raiden.blockchain.abi import CONTRACT_MANAGER
        CONTRACT_MANAGER.instantiate()


with open('README.md') as readme_file:
    readme = readme_file.read()


history = ''


install_requires_replacements = {
    "git+https://github.com/LefterisJP/pyethapp@raiden_pyethapp_fork#egg=pyethapp": "pyethapp",
    "git+https://github.com/LefterisJP/pyethereum@take_solidity_interface_into_account#egg=ethereum": "ethereum",
    "git+https://github.com/LefterisJP/pyelliptic@make_compatible_with_openssl1_1#egg=pyelliptic": "pyelliptic",
    "git+https://github.com/konradkonrad/pystun@develop#egg=pystun": "pystun",
}

install_requires = list(set(
    install_requires_replacements.get(requirement.strip(), requirement.strip())
    for requirement in open('requirements.txt') if not requirement.lstrip().startswith('#')
))

test_requirements = []

version = '0.0.5'  # preserve format, this is read from __init__.py

setup(
    name='raiden',
    version=version,
    description="",
    long_description=readme + '\n\n' + history,
    author='HeikoHeiko',
    author_email='heiko@brainbot.com',
    url='https://github.com/raiden-network/raiden',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    zip_safe=False,
    keywords='raiden',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    cmdclass={
        'test': PyTest,
        'compile_contracts': CompileContracts,
        'build_py': BuildPyCommand,
    },
    install_requires=install_requires,
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'raiden = raiden.__main__:main'
        ]
    }
)
