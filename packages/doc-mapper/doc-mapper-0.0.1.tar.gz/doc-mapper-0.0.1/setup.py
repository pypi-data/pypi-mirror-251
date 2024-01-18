from setuptools import setup, find_packages

setup(
    name='doc-mapper',
    version='0.0.1',
    description="Package to organize and visualize text for a bird's eye view of knowledge",
    author='Rintaro-Fukui',
    packages=find_packages(),
    license='MIT',
    install_requires = [
        'gensim==4.3.2',
        'ipython>=8.12.0',
        'numpy>=1.26.3',
        'scipy>=1.11.4',
        'setuptools>=69.0.3',
    ]
)
