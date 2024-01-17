from pathlib import Path

import os
import setuptools
from setuptools import Distribution
# from setuptools import find_packages


blacklist = ["__pycache__", ".DS_Store"]
# packages = ['omniORB', 'omniORBpy', 'bin', 'lib', 'share', 'include']
# packages=find_packages(where='/build-wheel', include=['bin', 'lib', 'share', 'include'])
package_dir={'': '/build-wheel'}


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


with open("/build-wheel/WheelDescription.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def files(path):
    result = []
    thisPath = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if not any(file in s for s in blacklist):
                thisPath.append(str(Path(f"{path}{os.path.sep}{file}")))
        else:
            if not any(file in s for s in blacklist):
                result += files(f"{path}{os.path.sep}{file}")
    result += [(path, thisPath)]
    print(result)
    return result


dataFiles = files("lib") + files("bin") + files("include") + files("share")

setuptools.setup(
    name="omniorb-py",
    version=os.getenv("RELEASE_VERSION"),
    author="Duncan Grisby",
    author_email="duncan@grisby.org",
    description="Ready to use omniorb distribution for unix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://omniorb.sourceforge.net/",
    data_files=dataFiles,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: POSIX",
    ],
    license="LGPL for libraries, GPL for tools",
    distclass=BinaryDistribution,
    python_requires=f">={os.getenv('PYTHON_FORMATTED_VERSION')}",
    package_dir=package_dir
)

