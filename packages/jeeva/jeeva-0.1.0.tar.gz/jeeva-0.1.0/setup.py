from setuptools import setup, find_packages

setup(
    name='jeeva',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'googlesearch-python',
        'spacy',
    ],
    entry_points={
        'console_scripts': [
            'jeeva = jeeva.jeeva:main',
        ],
    },
    author='Jeevanantham V',
    author_email='jeevanantham.v26@gmail.com',
    description='A handy application of web scrapping along with Named entity recognition.',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add any other classifiers relevant to your project
    ],
)
