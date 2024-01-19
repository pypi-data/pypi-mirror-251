
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='backwardsreg',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'statsmodels',
    ],
    entry_points={
        'console_scripts': [
            'your-command = backwardsreg.module:main',
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description='Backward Regression Python Library - Automated feature selection in linear and logistic regression models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kwadwo Daddy Nyame Owusu - Boakye',
    author_email='kwadwo.owusuboakye@outlook.com',
    url='https://github.com/knowusuboaky/backwardsreg',
    license='MIT',
)
