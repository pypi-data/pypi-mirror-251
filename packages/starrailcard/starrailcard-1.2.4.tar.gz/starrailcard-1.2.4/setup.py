from setuptools import setup, find_packages

setup(
    name='starrailcard',
    version='1.2.4',
    description='Module for generating Honkai Star Rail character cards',
    author='None',
    packages=find_packages(),
    install_requires=[
        'Pillow>=10.0.1',
        'honkairail>=1.1.4',
        'python>=3.9',
    ],
    extras_require={
        'dev': [
            'cachetools>=5.3.1',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'honkai', 'cards', 'generation', 'honkaistarraill', 'raill', 'starraill',
        'builds', 'honkairail', 'honkai'
    ],
    url='https://github.com/DEViantUA/StarRailCard',
    project_urls={
        'Source': 'https://github.com/DEViantUA/StarRailCard',
        'Documentation': 'https://github.com/DEViantUA/StarRailCard/blob/main/README.md',
    },
)
