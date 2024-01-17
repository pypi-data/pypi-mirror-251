from setuptools import setup, find_packages

setup(
    name='qweatherPyAPI',
    version='0.1.4',
    author='shaun',
    author_email='shaun.17g@gmail.com',
    packages=find_packages(),
    description='QWeatherPython API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shaun17/qweather-api.git',
    install_requires=[
        'requests',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)