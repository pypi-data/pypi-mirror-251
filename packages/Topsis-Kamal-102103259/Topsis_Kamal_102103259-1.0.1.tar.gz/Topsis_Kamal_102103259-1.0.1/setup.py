from setuptools import setup, find_packages

setup(
    name="Topsis_Kamal_102103259",
    version="1.0.1",
    author="Kamalpreet Kaur",
    author_email="kkamal101203@gmail.com",
    url="https://github.com/kkamal2003/Topsis_Kamal_102103259",
    description="A python package for implementing topsis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "numpy"],
    entry_points={"console_scripts": ["Topsis_Kamal_102103259 = src.main:main"]},
)