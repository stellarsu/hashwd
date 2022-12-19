from setuptools import setup, find_packages

setup(
    name='hashwd',
    version='0.2.13',
    license='GNUv3',
    author="Jordan Langland",
    author_email='root@gnom.me',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/stellarsu/hashwd',
    keywords='secure password generator',
    install_requires=[
          'pyperclip',
          'argparse',
          're'
      ],
          entry_points={
        'console_scripts': [
            'hashwd=hashwd:main'
        ]
        }
)