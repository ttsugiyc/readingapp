from setuptools import setup, find_packages

setup(
    name='readingapp',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask',
    ],
)
