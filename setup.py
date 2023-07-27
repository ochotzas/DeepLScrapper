from setuptools import setup, find_packages

setup(
    name='DeepLScrapper',
    version='1.5.2',
    description='An unofficial Python library for translating text using DeepL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Olger Chotza',
    author_email='olgerdev@icloud.com',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'fake-useragent'
    ],
    python_requires='>=3.9',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
