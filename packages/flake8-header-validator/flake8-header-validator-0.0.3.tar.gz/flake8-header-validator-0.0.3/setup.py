from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

classifiers = [
    'Framework :: Flake8',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Russian',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Software Development',
]

setup(
    name='flake8-header-validator',
    description='Check if python file contain copyright text',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=classifiers,
    author='Ben Donnelly',
    author_email='b.w.donnelly1@gmail.com',
    license='MIT',
    url='https://github.com/Umaaz/flake8-copyright-validator',
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'flake8',
        'importlib-metadata'
    ],
)
