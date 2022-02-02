import os
import re 

from setuptools import setup, find_packages


# borrowed from SQLAlchemy
with open(os.path.join(os.path.dirname(__file__), 'src', 'mapeathor', '_version.py')) as file:
    version = (re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S).match(file.read()).group(1))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as r:
    requirements = r.read().split("\n")[0:-1]

setup(
    name="mapeathor",
    version=version,
    author="Ana Iglesias-Molina",
    author_email="ana.iglesiasm@upm.es",
    license="Apache 2.0",
    description="Mapeathor is a simple spreadsheet parser able to generate mapping rules in three mapping languages: R2RML, RML (with extension to functions from FnO) and YARRRML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/Mapeathor",
    project_urls={
        'Documentation': 'https://github.com/oeg-upm/Mapeathor/wiki',
        'Source code': 'https://github.com/oeg-upm/Mapeathor/tree/master/src/mapeathor',
        'Issue tracker': 'https://github.com/oeg-upm/Mapeathor/issues',
    },
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
