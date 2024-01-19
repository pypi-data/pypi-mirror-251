from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='statstical-plot',
    version='0.1',
    license='MIT',
    author='Chen Liu',
    author_email='chen.liu.cl2482@yale.edu',
    packages={''},
    package_dir={'': 'src/'},
    description='Statistical plotting with good aesthetics.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ChenLiu-1996/StatsPlot',
    keywords='plotting, plot, statistical plotting, statistical plot',
    install_requires=['numpy', 'pandas', 'seaborn', 'matplotlib'],
)