from setuptools import setup, find_packages

VERSION = '1.1.4'
DESCRIPTION = 'Instaperq Product grpc package'
LONG_DESCRIPTION = 'This package contains the grpc proto generated files'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="instaperq",
    version=VERSION,
    author="Wesam Qaqish",
    author_email="wq@instaperq.ai",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'instaperqproductgrpc grpc package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)