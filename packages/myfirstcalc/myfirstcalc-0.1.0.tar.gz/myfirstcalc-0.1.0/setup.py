from setuptools import setup, find_packages

setup(
    name='myfirstcalc',
    version='0.1.0',
    packages=find_packages(include=['calculator', 'calculator.*']),
    entry_points={
        'console_scripts': ['calcdirect = calculator.calops:entry_point']
    }
)