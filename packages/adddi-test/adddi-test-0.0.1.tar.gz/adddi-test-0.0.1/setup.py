from setuptools import setup, find_packages

setup(
    name='adddi-test',
    version='0.0.1',
    description='PYPI tutorial package creation written by HBINKIM, addd inc.',
    author='hbinkim-addd',
    author_email='hbinkim@addd.co.kr',
    url='',
    install_requires=['tqdm', 'pandas', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['python tutorial', 'pypi'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)