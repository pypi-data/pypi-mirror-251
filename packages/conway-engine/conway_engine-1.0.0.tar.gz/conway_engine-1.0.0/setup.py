from setuptools import setup, find_packages

setup(
    name='conway_engine',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'game-of-life=conway_engine.simulation:main',
        ],
    },
    include_package_data=True,
    author='Vivek Dagar',
    author_email='vivekdagar2017@gmail.com',
    description="Conway Engine is a Python package offering a sophisticated implementation"
                " of Conway's Game of Life, featuring the iconic Gosper Glider Gun for dynamic"
                " and explosive cellular automaton growth.",
    url='https://github.com/vivekkdagar/conway_engine',
    license='GNU General Public License v3.0',
    long_description=open('PYPI_README.md').read(),
    long_description_content_type='text/markdown',
)
