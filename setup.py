from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py_bpmn',
    version='0.0.8',
    license='TBD',
    author='Vasudevan Palani',
    author_email='vasudevan.palani@gmail.com',
    url='https://github.com/vasudevan-palani/pybpmn',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pybpmn'],
    include_package_data=True,
    description="A bpmn framework focused on serverless infrastructure",
)
