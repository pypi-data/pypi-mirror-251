from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='disortify',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'disortify = disortify.__main__:main'
        ]
    },
    author='christian',
    author_email='christiang03112003@gmail.com',
    description='disortify python library for sorting,modifying and displaying data in various format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/christian0311/disortify',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
