from setuptools import setup, find_packages

setup(
    name='leandesk',
    version='1.8.0',
    packages=find_packages(),
    install_requires=[
      
    ],
    entry_points={
        'console_scripts': [
            'clean = LeanDesk.cli:main',
        ],
    },
)
