from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='DistroLab',
    version='0.2',
    author='Sylvester Kiranga',
    author_email='slynganga59@gmail.com',
    description='A package for Gaussian and Binomial distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Sylvester254/DistroLab',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
    ],
    zip_safe=False
)
