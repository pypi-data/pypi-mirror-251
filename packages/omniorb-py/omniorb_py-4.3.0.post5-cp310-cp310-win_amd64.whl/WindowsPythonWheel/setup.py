import sys
from pathlib import Path

import argparse
import glob
import sys
import os
import setuptools
from setuptools import Distribution

parser = argparse.ArgumentParser()
parser.add_argument('--release_version', required=True, type=str)
parser.add_argument('--omniorb_version', required=True, type=str)
args = parser.parse_args()

blacklist = ["__pycache__", ".DS_Store"]


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


with open("WindowsPythonWheel/WheelDescription.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def files(source_path, dest_path="Lib/site-packages"):
    result = []
    thisPath = []
    for file in os.listdir(source_path):
        if os.path.isfile(os.path.join(source_path, file)):
            if not any(file in s for s in blacklist):
                thisPath.append(str(Path(source_path) / file))
        else:
            if not any(file in s for s in blacklist):
                result += files(str(Path(source_path) / file), str(Path(dest_path) / file))
    result += [(dest_path, thisPath)]
    return result


python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
omniORBFolder = Path(f"WindowsPythonWheel/omniorb-versions/omniORBpy-{args.omniorb_version}_python{python_version}")
dllFilePaths = glob.glob(str(Path(omniORBFolder) / "lib" / "x86_win32" / "*"))
dllFilePaths.extend(glob.glob(str(Path(omniORBFolder) / "bin" / "x86_win32" / "*.dll")))

sys.argv = ["", "bdist_wheel"]

setuptools.setup(
    name="omniorb-py",
    version=args.release_version,
    author="Duncan Grisby",
    author_email="duncan@grisby.org",
    description="Ready to use omniorb distribution for windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://omniorb.sourceforge.net/",
    data_files=[("DLLs", dllFilePaths)] + files(source_path=str(Path(omniORBFolder) / "lib" / "python")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: Microsoft :: Windows",
    ],
    license="LGPL for libraries, GPL for tools",
    distclass=BinaryDistribution,
    python_requires='>=3.8'
)
