from setuptools import setup, find_packages

setup(
    name='tuits',
    version='0.1.0',
    author='William E. Doyle',
    author_email='contact.william.e.doyle@gmail.com',
    description='A CLI timesheet tool for managing tasks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wdoyle123/tuits.git',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'tuits': ['data/*.db'],
    },
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'tuits=tuits.tuits:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
