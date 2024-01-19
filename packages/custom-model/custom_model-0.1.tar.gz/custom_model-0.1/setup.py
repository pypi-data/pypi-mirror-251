from setuptools import setup, find_packages

setup(
    name='custom_model',
    version='0.1',
    packages=find_packages(),
    description='A custom model package',
    long_description="None",
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

