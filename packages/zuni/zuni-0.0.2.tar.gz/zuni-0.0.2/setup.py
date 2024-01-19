from setuptools import find_packages, setup

setup(
    name='zuni',
    packages=find_packages(include=['zuni']),
    version='0.0.2',
    description='Zillion Utility purpose Neural Interface',
    install_requires=['openai==1.3.8', 'together', 'angle-emb==0.3.1', 'qdrant-client'],
    author='azhan@brace.so',
)