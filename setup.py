from setuptools import setup


setup(
    name='zennolab_test',
    description='test case',
    author='Nick Markov',
    version="1.0.0",
    packages=[''],
    package_dir={'': 'src/zennolab'},
    install_requires=[
        'opencv-python==4.8.1.78',
        'tqdm==4.66.1',
        'pandas==2.0.3',
    ],
    entry_points={
        'console_scripts': [
            'run_evaluation = run_app:run_app',
        ]}
)
