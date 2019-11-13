# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import glob
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

import setuptools

here = abspath(dirname(__file__))
# We're using a pip8 style requirements file, which allows us to embed hashes
# of the packages in it. However, setuptools doesn't support parsing this type
# of file, so we need to strip those out before passing the requirements along
# to it.
with open(join(here, "requirements", "base.txt")) as f:
    requirements = []
    for line in f:
        # Skip empty and comment lines
        if not line.strip() or line.strip().startswith("#"):
            continue
        # Skip lines with hash values
        if not line.strip().startswith("--"):
            requirements.append(line.split(";")[0].split()[0])
            requirement_without_python_filter = line.split(";")[0]
            requirement_without_trailing_characters = requirement_without_python_filter.split()[0]

with open(join(here, "requirements/test.in")) as f:
    tests_require = [i.strip() for i in f.readlines() if i and not i.startswith("-r")]

with open("version.txt") as f:
    VERSION = f.read().strip()


setuptools.setup(
    name="mozilla-mapper-api",
    version=VERSION,
    description="The code behind https://mapper.mozilla-releng.net/",
    author="Mozilla Release Engineering Team",
    author_email="release+mapper@mozilla.com",
    url="https://mapper.mozilla-releng.net",
    tests_require=tests_require,
    install_requires=requirements,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    license="MPL2",
)
