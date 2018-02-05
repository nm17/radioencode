from setuptools import setup

setup(
    name='radioencode',
    version='0.2',
    packages=['radioencode'],
    url='https://github.com/NeverMine17/radioencode',
    license='MIT',
    author='NeverMine17',
    author_email='dannevergame@gmail.com',
    description='Convert morse code into sound',
    entry_points={
        'console_scripts': [
            'radioencode = radioencode:main',
        ],
    }
)
