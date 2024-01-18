from setuptools import setup, find_packages

setup(
    name="test-packages-sdp",
    version="0.0.1",
    author="Devadarshini",
    author_email="darun@lululemon.com",
    description="An application that informs you of the time in different locations and timezones",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["test-packages-sdp = src.main:main"]},
)
