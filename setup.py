from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    Returns a list of requirements from a requirements file.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        List[str]: A list of requirements.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name='Adobe Round 1',
    version='0.0.1',
    author='Aman Raghuwanshi',
    author_email='r.aman@iitg.ac.in',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
