from setuptools import setup, find_packages

VERSION = '1.1.5' 
DESCRIPTION = 'Toolkits for text processing and augmentation for Bangla NLP'

setup(
        name="banglanlptoolkit", 
        version=VERSION,
        author="A F M Mahfuzul Kabir",
        author_email="<afmmahfuzulkabir@gmail.com>",
        description=DESCRIPTION,
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        classifiers = [
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
        keywords=['Bangla NLP','Bangla','NLP','NLP Toolkit','Bengali NLP','Bengali Augmentation','Bengali Text Normalization','Bangla NLP Toolkit','Bangla Punctuation'],
        url='https://github.com/Kabir5296/banglanlptoolkit',
        project_urls={'Repository': 'https://github.com/Kabir5296/banglanlptoolkit'},
)