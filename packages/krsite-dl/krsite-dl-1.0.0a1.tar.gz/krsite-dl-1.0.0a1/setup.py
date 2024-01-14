"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import os
import warnings


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, encoding="utf-8") as f:
        return f.read()

def check_file(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(path):
        return True
    warnings.warn(f"File: {fname} not found. So not included.")


PACKAGES = [
    "krsite_dl",
    "krsite_dl.common",
    "krsite_dl.client",
    "krsite_dl.extractor",
    "krsite_dl.down",
]

DESC = "Download images from korean site and press at the highest quality."
# Get the long description from the README file
LONG_DESC = read("readme.md")

VERSION = '1.0.0a1'


def build_setuptools():
    from setuptools import setup, find_packages
    setup(
        name="krsite-dl",
        version=VERSION,
        description=DESC,
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/zer0kn0wledge/krsite-dl",
        author="zer0kn0wledge",  # Optional
        author_email="neptunemist@proton.me",  # Optional

        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Operating System :: OS Independent",
            "Topic :: Utilities",
            "Topic :: Multimedia :: Graphics",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3 :: Only",
        ],
       
        keywords="sbs, naver, naverpost, image, media, downloader, scrapper",

        packages=PACKAGES,
        python_requires=">=3.7, <4",
        # This field lists other packages that your project depends on to run.
        # Any package you put here will be installed by pip when your project is
        # installed, so they must be valid existing projects.
        #
        # For an analysis of "install_requires" vs pip's requirements files see:
        # https://packaging.python.org/discussions/install-requires-vs-requirements/
        install_requires=["requests"],  # Optional
        # List additional groups of dependencies here (e.g. development
        # dependencies). Users will be able to install these using the "extras"
        # syntax, for example:
        #
        #   $ pip install sampleproject[dev]
        #
        # Similar to `install_requires` above, these must be valid existing
        # projects.
        # extras_require={  # Optional
        #     "dev": ["check-manifest"],
        #     "test": ["coverage"],
        # },
        # If there are data files included in your packages that need to be
        # installed, specify them here.
        # package_data={  # Optional
        #     "sample": ["package_data.dat"],
        # },
        entry_points={  # Optional
            "console_scripts": [
                "krsite-dl=krsite_dl:main",
            ],
        },
        project_urls={  # Optional
            "Bug Reports": "https://github.com/zer0kn0wledge/krsite-dl/issues",
            "Funding": "https://donate.pypi.org",
            "Say Thanks!": "http://saythanks.io/to/example",
            "Source": "https://github.com/zer0kn0wledge/krsite-dl",
        },
    )

build_setuptools()