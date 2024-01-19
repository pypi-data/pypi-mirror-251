from setuptools import find_packages, setup

setup(
    name='zuni',
    packages=find_packages(include=['zuni']),
    version='0.0.3',
    description='Zillion Utility purpose Neural Interface',
    install_requires=['openai==1.3.8', 'together', 'peft==0.7.1', 'angle-emb==0.3.1', 'qdrant-client'],
    author='azhan@brace.so',
)