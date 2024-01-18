from setuptools import setup, find_packages

setup(
    name='pearwise',
    version='0.1.2',
    packages=find_packages(),
    description='PearWiseAI SDK to log and score interactions',
    author_email='hello@pearwise.com',
    author="pearwise",
    install_requires=[
        'requests',
        'pydantic',
    ],
    
)
