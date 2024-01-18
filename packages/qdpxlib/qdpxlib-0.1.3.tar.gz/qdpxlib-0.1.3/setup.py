from setuptools import setup, find_packages

setup(
    name="qdpxlib",
    version="0.1.3",
    author="Ori Yonay, Anwesha Basu, Carlos Morales, Texas A&M Center for Teaching Excellence",
    author_email="oyonay12@tamu.edu",
    description="Easy QDPX (MAXQDA) file handling",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/oriyonay/aqc",
    package_dir={'': 'src'}, 
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
