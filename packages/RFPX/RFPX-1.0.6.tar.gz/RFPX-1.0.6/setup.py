from setuptools import setup, find_packages

with open(file='pxapp/README.md', mode='r') as f:
    description = f.read()

setup(
    name='RFPX',
    version='1.0.6',
    description="A helping tool",
    package_dir={"": "pxapp"},
    packages=find_packages(where="pxapp"),
    long_description=description,
    long_description_content_type="text/markdown",
    author="rf123",
    license="RFPX Software Subscription Agreement",
    install_requires=["bson >= 0.5.10",
                      "twine>=4.0.2",
                      ],
    python_requires=">=3.9"
)

# Test pypi api
# pypi-AgENdGVzdC5weXBpLm9yZwIkMjc2NDFlMjEtNDBmZi00OGViLTg1OTctZDQ0NDkxMWM5ZGZhAAIqWzMsIjY3OTFmN2QzLTQzMGEtNDYxMi1iYzkxLWU2YzNjMWI1ZmJlZCJdAAAGIEbWOD8berk0pKfl8y0X77hH01s5_QN4t8wPHi14I8bN
# twine upload -r testpypi dist/*

# Real pypi api
#pypi-AgEIcHlwaS5vcmcCJDRjMDZjMGFhLWZhYjgtNDRjZi05MWI3LWI3MWJkOTZjYzMyMAACKlszLCI3MTgzYWI5OS1kZTIzLTQxMjgtYWZmMi0zNzcyODA3MGEzYzYiXQAABiC9oE3LzRTqx8swBUq6FfFhbYdcGvugCi6TVuZ7aF1gzg