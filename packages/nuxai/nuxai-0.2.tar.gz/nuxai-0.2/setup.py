
from setuptools import setup, find_packages


setup(
    name='nuxai',
    version='0.2',
    license='MIT',
    author="Ethan Steininger",
    author_email='ethan@nux.ai',
    packages=['nuxai'],
    url='https://github.com/nux-ai/nux-python',
    keywords='LLM Pipelines',
    description='llm pipelines',
    install_requires=['requests']
)
