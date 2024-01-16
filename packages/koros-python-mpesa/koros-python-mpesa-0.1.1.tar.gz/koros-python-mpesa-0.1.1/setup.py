from setuptools import setup, find_packages

setup(
    name='koros-python-mpesa',
    version='0.1.1',
    author='Kevin Ongulu',
    author_email='kevinongulu@gmail.com',
    description='A python package for connecting to MPESA APIs',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)