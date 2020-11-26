import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dynv6_ddns',
    version='0.0.1',
    author='Rafael J. Vicente',
    author_email='rafaelj.vicente@gmail.com',
    description='Python client to update dynv6.com using the provided Rest API with a token',
    long_description=long_description,
    url='https://github.com/RafaelJVicente/dynv6_ddns',
    packages=setuptools.find_packages(),
    install_requires=['uri'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
