from setuptools import setup, find_packages

setup(
    name='apipulse-sdk',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    description='Api automation testing sdk for django framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/your-middleware',
    author='Vikram Panwar',
    author_email='vikram.panwar@apipulse.dev',
    license='unlicensed',
    install_requires=[
        'Django>=3.0',
        # testing addtional packages
        'requests',
        'pydantic'
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        "License :: Other/Proprietary License",
    ],
)
