import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='vasp-fw',
    version='0.1.0',
    description='A bridge between vasp and fireworks',
    long_description="This package bridges together fireworks and VASP",

    long_description_content_type='text/x-rst',
    url='https://github.com/kul-group/vasp-fw',
    author='Dexter Antonio',
    author_email='dexter.d.antonio@gmail.com',
    license="MIT",
    packages=['vaspfw'],
    include_package_data=True,
    install_requires=['ase', 'numpy', 'typing'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='ase zeolites vasp simulation',
    project_urls={
        'Documentation': 'https://kul-group.github.io/MAZE-sim/build/html/index.html',
        'Source': 'https://github.com/kul-group/MAZE-sim/',
        'Tracker': 'https://github.com/kul-group/MAZE-sim/issues',
    },
    python_requires='>=3.7'
)
