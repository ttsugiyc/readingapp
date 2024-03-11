from setuptools import setup, find_packages

setup(
    name='readingapp',
    version='1.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask',
        'waitress',
    ],
)
