import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MergeGI",
    version="0.0.1",
    author="Sequana Team",
    description="Merge MGI fastq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sequana/MergeGI",
    project_urls={
        "Bug Tracker": "https://github.com/sequana/MergeGI/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix"
    ],
    packages=setuptools.find_packages(where="mergegi"),
    python_requires=">=3.6",
    install_requires=open("requirements.txt").read(),
    tests_requires=['pytest'],
    entry_points={
        'console_scripts': [
            'mergegi=mergegi:main',
        ],
    },
)
