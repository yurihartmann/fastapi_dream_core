from setuptools import setup
from fastapi_dream_core import __version__

setup(
    name='fastapi_dream_core',
    version=__version__,
    author='Yuri Hartmann',
    author_email='yurihartmann0607@gmail.com',
    description='Reusable core, repositories and utilities for FastAPI',
    url='https://github.com/yurihartmann/fastapi_dream_core',
    project_urls={
        'Código fonte': 'https://github.com/yurihartmann/fastapi_dream_core',
    },
    install_requires=[
        'fastapi',
        'sqlmodel',
        'sqlalchemy',
        'pydantic'
    ],
    license='MIT',
    keywords='fastapi_dream_core core api',
)
