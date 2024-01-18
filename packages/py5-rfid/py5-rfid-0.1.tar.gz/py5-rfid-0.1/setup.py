from setuptools import setup, find_packages

setup(
    name='py5-rfid',
    version='0.1',
    author="M.Karthickraja",
    author_email="karthickrajam8100@gmail.com",
    description="Raspberry pi 5 interface with RFID(MFR522)",
    packages=find_packages(),
    install_requires=[
        'gpiod',
        'time',
        'spidev',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)