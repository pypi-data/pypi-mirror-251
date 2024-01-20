from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis_Kamal_102103259",
    version="1.0.13",
    author="Kamalpreet Kaur",
    author_email="kkamal101203@gmail.com",
    url="https://github.com/kkamal2003/Topsis_Kamal_102103259",
    description="A python package for implementing topsis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "numpy"],
    entry_points={"console_scripts": ["Topsis_Kamal_102103259 = Topsis_Kamal_102103259.main:main"]},
)