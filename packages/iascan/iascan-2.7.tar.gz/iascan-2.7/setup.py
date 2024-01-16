from setuptools import setup, find_packages

setup(
    name='iascan',
    version='2.7',
    author='Itibar Aheshman',
    author_email='aheshman.itibar@gmail.com',
    packages=find_packages(),
    description='A simple IP scanner tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GeekMada/iascan.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'iascan=iascan.main:main',
        ],
    },
)