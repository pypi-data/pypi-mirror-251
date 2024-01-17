from setuptools import setup, find_packages

setup(
    name='mm_download_img',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author="Viet Nguyen Ba",
    author_email="nbviet98@gmail.com",
    description="A library to download image from s3",
    entry_points={
        'console_scripts': [
            # If your library includes any command-line scripts, list them here
        ],
    },
    # url='https://your-private-repo-url',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)