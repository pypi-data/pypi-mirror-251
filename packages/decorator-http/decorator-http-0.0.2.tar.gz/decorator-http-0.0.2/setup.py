from setuptools import setup, find_packages

setup(
    name='decorator-http',
    version='0.0.2',
    author='Paulo Henrique',
    author_email='contact@paulohenriquesn.com',
    description='A easy way to use requests but with decorators',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
