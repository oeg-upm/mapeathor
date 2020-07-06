import setuptools
import time

v_time = str(int(time.time()))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as r:
    requirements = r.read().split("\n")[0:-1]

setuptools.setup(
    name="mapeathor",
    version="1.0.0."+v_time,
    author="Ana Iglesias-Molina",
    author_email="ana.iglesiasm@upm.es",
    license="Apache 2.0",
    description="Mapeathor is a simple spreadsheet parser able to generate mapping rules in three mapping languages: R2RML, RML (with extension to functions from FnO) and YARRRML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/Mapeathor",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
