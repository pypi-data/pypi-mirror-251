from setuptools import setup

setup(
    name='ThisPackageIsDataTransfer',
    version='1.7',
    packages=[
        'DataTransfer',
        'DataTransfer/network',
        'DataTransfer/transferer'
    ],
    entry_points={
        'console_scripts': [
            'transfer=DataTransfer.main:main'
        ]
    }
)