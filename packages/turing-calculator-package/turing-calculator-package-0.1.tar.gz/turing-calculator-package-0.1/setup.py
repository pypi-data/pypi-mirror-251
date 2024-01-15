from setuptools import setup, find_packages

setup(
    name='turing-calculator-package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'mypy>=1.8.0',
        'mypy-extensions>=1.0.0',
        'packaging>=23.2',
        'pyflakes>=3.2.0',
        'pytest>=7.4.4',
        'typing_extensions==4.9.0'

    ],
    author='M Usman Tahir',
    author_email='usmantahir78@gmail.com',
    description='This Python package provides a simple calculator with basic mathematical operations',
    long_description='This Python package provides a simple calculator with basic mathematical operations as per the sprint one assingment. Following requirments has been implemented in the code.',
    url='https://github.com/TuringCollegeSubmissions/utahir-DWWP.1.5',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)
