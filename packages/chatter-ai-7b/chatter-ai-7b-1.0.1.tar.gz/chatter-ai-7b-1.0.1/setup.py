
from setuptools import setup, find_packages
f = open("README.md")
long_desc = f.read()
f.close()
if __name__ == '__main__':
    setup(
        name='chatter-ai-7b',
        version="1.0.1",
        packages=find_packages('.', include=['chatter_ai*']),
        description='A chatter AI.',
        long_description=long_desc,
        long_description_content_type='text/markdown',
        install_requires=[
              "requests",
        ]
    )
