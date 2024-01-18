from setuptools import setup, find_packages

setup(
    name='generate-score',
    version='2021.8',
    author='Erik Scheffers',
    author_email='e.t.j.scheffers@tue.nl',
    description="Calculate score",
    url='https://momotor.org/',
    install_requires=[
        'momotor-bundles~=4.0',
        'mtrchk-org-momotor-base~=1.0',
    ],
    python_requires='>=3.7',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=True,
    entry_points={
        'momotor.checklet': [
            'generate-score = generate_score:GenerateScore',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: Other/Proprietary License',
    ],
)
