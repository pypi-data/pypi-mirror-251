from setuptools import setup 

setup(
    name="logical-package",  # Required
    version="1.0.0",  # Required
    long_description=" long dec", 
    packages= ['src'],
    python_requires=">=3.7, <4",
    install_requires=["pymongo" , "python-binance"],  # Optional
)