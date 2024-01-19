from setuptools import find_packages, setup

README = open("README.md").read()

setup(
    name='exclusiveAI',
    packages=find_packages(),
    version='0.0.1b',
    long_description_content_type="text/markdown",
    url="https://github.com/exclusiveAI/MLProject",
    long_description=README,
    author_email='chuckpaul98@icloud.com',
    install_requires=['numpy', 'matplotlib', 'pandas', 'tqdm', 'joblib', 'wandb'],
    description='An inefficient (for the moment) neural network with numpy',
    setup_requires=['pytest-runner'],
    author='Paul Magos & Francesco Paolo Liuzzi',
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)