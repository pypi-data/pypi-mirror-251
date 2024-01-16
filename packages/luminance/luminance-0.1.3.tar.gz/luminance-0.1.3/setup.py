from setuptools import setup, find_packages

setup(
    name='luminance',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    author='Artem Reslaid',
    description='Luminance is a library for working with user output and console input',
    license='MIT',
    long_description=open('luminance/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/reslaid/luminance',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
