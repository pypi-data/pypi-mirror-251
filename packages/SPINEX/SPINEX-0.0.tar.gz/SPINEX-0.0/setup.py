from setuptools import setup, find_packages

setup(
    name='SPINEX',
    version='0.000',
    packages=find_packages(),
    description='A Python package for SPINEX algorithm',
    url='https://arxiv.org/abs/2306.01029',
    long_description=open('Readme/README.md').read(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
    ],
    python_requires='>=3.6',
)
