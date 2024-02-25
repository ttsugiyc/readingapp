from setuptools import setup, find_packages

setup(
    name='readingapp',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask',
        'waitress',
    ],
)
