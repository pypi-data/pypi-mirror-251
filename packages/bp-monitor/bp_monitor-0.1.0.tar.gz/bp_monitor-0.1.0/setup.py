from setuptools import setup, find_packages

# Read the contents of requirements.txt from package root
# with open('requirements.txt') as f:
#     install_requires = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='bp_monitor',
    version='0.1.0',
    author='Sudhir Arvind Deshmukh',
    description='Allows use to input bloood pressure vaules and creates reports including visualisations indicating BP treds over time',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bokey007/bp_monitor',
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.3',
        'plotly==5.13.1',
        'reportlab==4.0.9',
        'streamlit==1.13.0',
    ],
    entry_points={
        'console_scripts': [
            'bp_monitor.run=bp_monitor.run:run',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

#how to build test and bublish this pkg

# pip uninstall bp_monitor
# python setup.py sdist bdist_wheel
# pip install ./dist/bp_monitor-0.1.0.tar.gz
# bp_monitor.run
# twine upload dist/*