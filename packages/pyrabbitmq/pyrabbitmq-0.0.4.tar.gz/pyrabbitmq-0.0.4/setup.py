from setuptools import setup

setup(
    name='pyrabbitmq',
    version='0.0.4',
    author='Xizhen Du',
    author_email='xizhendu@gmail.com',
    url='https://github.com/xizhendu/pyrabbitmq',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    description='Simple Python client library for RabbitMQ',
    packages=['pyrabbitmq'],
    install_requires=[
        "requests",
    ]
)
