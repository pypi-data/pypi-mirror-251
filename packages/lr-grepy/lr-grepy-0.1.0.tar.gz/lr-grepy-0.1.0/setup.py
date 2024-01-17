from setuptools import setup, find_packages

setup(
    name='lr-grepy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'grepy=grepy.cli:main',
        ],
    },
    author='literank',
    license='MIT',
    description='An example project\'s grep-like CLI app \
        implemented in Python.',
    url='https://github.com/Literank/lr_grepy',
)
