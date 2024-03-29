import itertools
import os
import platform
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import contextmanager

from setuptools import Distribution, find_packages, setup

try:  # python 3
    import winreg
    from urllib.request import urlretrieve
except ImportError:  # python 2
    import _winreg as winreg
    from urllib import urlretrieve


MSVC_MIN_VERSION = (14, 0, 24215)


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


def is_msvc_redist_installed(major, minor, build):
    if platform.machine().endswith("64"):  # check if os is 64bit
        sub_key = "SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64"
    else:
        sub_key = "SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x86"
    try:
        key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key)
        runtime_installed = winreg.QueryValueEx(key_handle, "Installed")[0]
        installed_major = winreg.QueryValueEx(key_handle, "Major")[0]
        installed_minor = winreg.QueryValueEx(key_handle, "Minor")[0]
        installed_build = winreg.QueryValueEx(key_handle, "Bld")[0]
        return (
            runtime_installed != 0
            and installed_major >= major
            and installed_minor >= minor
            and installed_build >= build
        )
    except WindowsError as exc:
        return False

with open("README.md", "r") as fh:
    long_description = fh.read()

def install_msvc_redist():
    url = (
        "https://download.microsoft.com/download/6/A/A/"
        "6AA4EDFF-645B-48C5-81CC-ED5963AEAD48/vc_redist.x86.exe"
    )
    dl_dir = tempfile.mkdtemp()
    dl_file = os.path.join(dl_dir, "vc_redist.exe")
    urlretrieve(url, dl_file)
    subprocess.call([dl_file, "/quiet"])
    # trying to remove the temp folder triggers
    # an error during py2 pip install


if not is_msvc_redist_installed(*MSVC_MIN_VERSION):
    install_msvc_redist()

# The version string is substituted in by CMake.
setup(
    name="libloot-python",
    version="@LIBLOOT_PY_VERSION_MAJOR@.@LIBLOOT_PY_VERSION_MINOR@.@LIBLOOT_PY_VERSION_PATCH@",
    description="A Python module that wraps libloot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loot/libloot-python",
    packages=find_packages(),
    include_package_data=True,
    package_data={"loot": ["loot*.pyd", "loot.dll"]},
    distclass=BinaryDistribution,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++'
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.7',
)
