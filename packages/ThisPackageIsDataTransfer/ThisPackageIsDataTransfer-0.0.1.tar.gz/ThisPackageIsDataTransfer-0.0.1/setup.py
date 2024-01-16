from setuptools import setup

setup(
    name='ThisPackageIsDataTransfer',
    version='0.0.1',
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