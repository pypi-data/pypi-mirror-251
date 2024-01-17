from setuptools import setup, find_packages

setup(
    name='denari',
    version='1.0.47',
    description='DenariAnalytics OpenSource Business and Tax Tools',
    author='Fadil Karim',
    author_email='fid_kk@proton.me',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'dash'
    ],
    package_data={
        'denari': ['Tax Tables/**/*']
    }

)