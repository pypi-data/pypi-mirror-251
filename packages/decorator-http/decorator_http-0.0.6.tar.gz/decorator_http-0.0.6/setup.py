from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='decorator_http',
    version='0.0.6',
    author='Paulo Henrique',
    author_email='contact@paulohenriquesn.com',
    description='A easy way to use requests but with decorators',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=['decorator_http'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
)
