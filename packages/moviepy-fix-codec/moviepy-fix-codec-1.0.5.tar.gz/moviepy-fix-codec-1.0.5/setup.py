#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'moviepy-fix-codec'
DESCRIPTION = 'moviepy-fix-codec.'
URL = 'https://github.com/SherlockGougou/moviepy-fix-codec'
EMAIL = 'qinglingou@gmail.com'
AUTHOR = 'SherlockGougou'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.5'

# What packages are required for this module to be executed?
REQUIRED = [
    "decorator>=4.0.2,<6.0",
    "imageio>=2.5,<3.0",
    "imageio_ffmpeg>=0.2.0",
    "numpy>=1.17.3",
    "proglog<=1.0.0",
]

optional_reqs = [
    "pygame>=1.9.3",
    "python-dotenv>=0.10",
    "opencv-python",
    "scikit-image",
    "scikit-learn",
    "scipy",
    "matplotlib",
    "youtube_dl",
]

doc_reqs = [
    "numpydoc<2.0",
    "Sphinx==3.4.3",
    "sphinx-rtd-theme==0.5.1",
]

test_reqs = [
    "coveralls>=3.0,<4.0",
    "pytest-cov>=2.5.1,<3.0",
    "pytest>=3.0.0,<7.0.0",
]

lint_reqs = [
    "black>=22.3.0",
    "flake8>=4.0.1",
    "flake8-absolute-import>=1.0",
    "flake8-docstrings>=1.6.0",
    "flake8-rst-docstrings>=0.2.5",
    "flake8-implicit-str-concat==0.3.0",
    "isort>=5.10.1",
    "pre-commit>=2.19.0",
]

# What packages are optional?
EXTRAS = {
    "optional": optional_reqs,
    "doc": doc_reqs,
    "test": test_reqs,
    "lint": lint_reqs,
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["docs", "tests"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Multimedia :: Video :: Conversion",
    ],
    keywords="video editing audio compositing ffmpeg",
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
    command_options={
        "build_docs": {
            "build_dir": ("setup.py", "./docs/build"),
            "config_dir": ("setup.py", "./docs"),
            "version": ("setup.py", VERSION.rsplit(".", 2)[0]),
            "release": ("setup.py", VERSION),
        }
    },
)