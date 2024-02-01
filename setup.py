from setuptools import setup, find_packages

setup(
    name='NanoPsiPy',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    scripts=["bin/NanoPsiPy_estimation", "bin/NanoPsiPy_comparison"],
    install_requires=[
        'numpy>=1.24.0',
        'pandas>=1.1.0',
        ],
    license="GPL 3.0"
)
