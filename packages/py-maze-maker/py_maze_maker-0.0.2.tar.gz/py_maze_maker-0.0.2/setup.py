from setuptools import setup, find_packages

setup(
    name='py_maze_maker',
    version='0.0.2',
    author='Mohammad Sajid Anwar',
    author_email='mohammad.anwar@yahoo.com',
    description='A simple Python package to make ASCII maze.',
    packages=find_packages(),
    scripts=[
        'scripts/maze-maker'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
