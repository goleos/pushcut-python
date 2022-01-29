from setuptools import setup

install_requires = [
        "requests==2.26.0"
    ]

setup(
    name='pushcut',
    version='0.0.1',
    packages=['pushcut'],
    install_requires=install_requires,
    python_requires='>3.5'
)