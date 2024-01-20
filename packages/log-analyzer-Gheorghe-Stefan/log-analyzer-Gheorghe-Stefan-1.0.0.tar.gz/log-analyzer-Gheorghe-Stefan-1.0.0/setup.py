from setuptools import setup, find_packages

setup(
    name='log-analyzer-Gheorghe-Stefan',
    version='1.0.0',
    description='Your package description',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    package_data={
        '': ['CHANGELOG.txt'],
    },
    include_package_data=True,
)
