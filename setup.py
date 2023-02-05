from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bempy',
    version='0.1',
    description='BEM-based class construction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/fefa4ka/python-bem',
    author='Alexander Kondratev',
    author_email='alex@nder.work',
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
