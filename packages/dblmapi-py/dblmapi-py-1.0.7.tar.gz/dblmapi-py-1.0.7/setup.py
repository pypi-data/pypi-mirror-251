from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='dblmapi-py',
    version='1.0.7',  # Update version to match your intended version
    author='Mindset',
    author_email='Noahswim111@gmail.com',
    description='A Python module for modding Dragon Ball Legends',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JuJutsuCord/DBLMAPI/',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'dblmapi=dblmapi.src.dblmapi_cli:main',  # Update the entry point here
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
