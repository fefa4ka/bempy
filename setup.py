from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bempy',
    version='0.3.2',
    description='BEM-based class construction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/fefa4ka/bempy',
    author='Alexander Kondratev',
    author_email='alex@nder.work',
    license='GPLv3+',
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'bempy=bempy.cli:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_data={
        'bempy': ['docs/**/*.md'],
    },
    include_package_data=True,
)

