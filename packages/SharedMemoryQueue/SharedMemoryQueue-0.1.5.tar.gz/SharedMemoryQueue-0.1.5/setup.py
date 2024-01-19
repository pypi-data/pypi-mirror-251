from setuptools import setup, find_packages

setup(
    name='SharedMemoryQueue',
    version='0.1.5',
    author='Natália Bruno Rabelo',
    author_email='natynbr@hotmail.com',  
    description='A Python library for interacting with a shared memory queue via C++ DLL.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
    ],
    python_requires='>=3.6',
    include_package_data=True,
    data_files=[('libs', ['libs/SharedQueue.dll'])]
)
