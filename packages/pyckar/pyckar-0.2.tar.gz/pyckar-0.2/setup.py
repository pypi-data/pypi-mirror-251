from setuptools import setup, find_packages

setup(
    name='pyckar',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts":[
            "pyckar=pyckar:hello",
    ],
},
)
