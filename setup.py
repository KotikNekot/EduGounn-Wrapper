from setuptools import setup, find_packages

setup(
    name='pyedugounn',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/KotikNekot/EduGounn-Wrapper',
    license='MIT',
    author='whynotvoid',
    description='A Python wrapper for the EduGounn school diary system, available only in Nizhny Novgorod region.',
    long_description_content_type='text/markdown',
    install_requires=[
        'aiohttp',
        'pydantic',
    ],
    python_requires='>=3.10',
)
