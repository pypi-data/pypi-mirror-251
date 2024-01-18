from setuptools import setup, find_packages

setup(
    name='yeedu-cli',
    packages=find_packages(),
    install_requires=[
        'argparse==1.4.0',
        'requests==2.28.1',
        'python-dotenv==1.0.0',
        'PyYAML==6.0',
        'setuptools==59.6.0'
    ],
    version='1.0.0',
    entry_points='''
    [console_scripts]
    yeedu=yeedu:yeedu
    '''
)
