from setuptools import setup, find_packages, find_namespace_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()


setup(
    name='RNAxtract',
    version='0.0.1',
    description = 'Splitting barcodes from RNA direct sequencing signals using Oxford Nanopore',
    author="Lian Lin",
    author_email='21620151153308@stu.xmu.edu.cn',
    license='GPL3',
    keywords='barcode split',
    include_package_data=True,
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"RNAxtract.model": ["*.hdf5"]},
    install_requires=install_requires,
    scripts=['src/RNAxtract/rnabs.py']
)
