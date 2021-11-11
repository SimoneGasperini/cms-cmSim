from setuptools import setup, find_packages


def get_requirements():
    with open('./requirements.txt', mode='r') as f:
        reqs = f.read().splitlines()
    return reqs


setup(
    name='CMS-cmSim',
    author='SimoneGasperini',
    author_email='simone.gasperini2@studio.unibo.it',
    version='0.0.1',
    url='https://github.com/SimoneGasperini/cms-cmSim',
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires='>=3.8',
)
