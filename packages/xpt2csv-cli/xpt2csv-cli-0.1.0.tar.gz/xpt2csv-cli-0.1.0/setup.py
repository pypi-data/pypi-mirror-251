
from setuptools import find_packages, setup

setup(
    name='xpt2csv-cli',
    packages=find_packages(include= ['xpt2csv']),
    version='0.1.0',
    install_requires=['pyreadstat',
                      'click'],
    description='CLI app to convert xpt file to csv',
    entry_points='''
    [console_scripts]
    to_csv=xpt2csv.to_csv:xpt_to_csv
    ''',
    author='Yousuf Ali',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
