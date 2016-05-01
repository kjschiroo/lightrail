from setuptools import setup

setup(
    name='Lightrail',
    version='0.1',
    description='Module for monitoring twin cities lightrail',
    url='https://github.com/kjschiroo/Lightrail',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',

    packages=['lightrail'],
    install_requires=['pyfiglet', 'docopt']
)
