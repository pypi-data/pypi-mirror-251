from setuptools import setup, find_packages

setup(
    name='TurtleExtentions',
    version='0.1.0',
    author='Pai',
    author_email='irisdamodder@gmail.com',
    description='Extention of the built in Turtle package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "Turtle"
    ],
    python_requires='>=3.8',
)