from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='ferramentas',
    version='1.0',
    description='ahuashuahus',
    long_description=Path('README.md').read_text(),
    author='Daniel',
    author_email='daniel@gmail.com',
    keywords=['camera', 'video', 'processamento'],
    packages=find_packages()
)