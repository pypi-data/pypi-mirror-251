from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mm_download_img',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        "opencv-python"
    ],
    author="Viet Nguyen Ba",
    author_email="nbviet98@gmail.com",
    description="A library to download image from s3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            # If your library includes any command-line scripts, list them here
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)