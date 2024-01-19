from setuptools import setup, find_packages


setup(
    name='EntityExtractor',
    author='Ankit Mor',
    version='0.2',
    packages=find_packages(),
    description='Extract specific entites from a text. Give text and get a json formatted output data.',
    long_description=open('Readme.md').read(), 
    long_description_content_type='text/markdown',
    install_requires=['pandas>=2.0.3', 'numpy>=1.24.3', 'nltk>=3.8.1', 'requests', 'BeautifulSoup4','spacy>=3.7.2'],
    
)