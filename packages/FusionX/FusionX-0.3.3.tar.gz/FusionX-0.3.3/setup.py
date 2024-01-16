import setuptools
from setuptools import setup, find_packages
install_deps = ['numpy>=1.20.0', 'opencv-python>=4.8.1.78']
VERSION = 'V0.3.3'
DESCRIPTION = 'fusionX'

# Setting up
setup(
    name="FusionX",
    version=VERSION,
    author="Bar Ben David, Suman Khan",
    author_email="FusionX_pipeline@hotmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="""
    A deep learning pipeline for cell-cell fusion analysis

    Authors: Bar Ben David, Suman Khan
    Email: FusionX_pipeline@hotmail.com
    """,

    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_deps,
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
          'FusionX = FusionX.__main__:main']
        
    },
)
