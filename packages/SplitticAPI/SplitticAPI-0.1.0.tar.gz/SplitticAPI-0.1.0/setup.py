from setuptools import setup, find_packages

setup(
    name='SplitticAPI',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'asyncio',
        'httpx',
        'Pillow',
        'requests',
    ],
)
