import os
import re
from pathlib import Path
from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def get_version():
    init = open(os.path.join(this_directory, 'src', 'superannotate_schemas', '__init__.py')).read()
    match = re.search(r'^__version__ = [\'"]([^\'"]+)[\'"]', init, re.M)
    if not match:
        raise RuntimeError('Unable to find version string.')
    return match.group(1)


setup(
    name='superannotate_schemas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=get_version(),
    package_dir={"": "src"},
    data_files=[('superannotate_schemas/schemas', [
        'src/superannotate_schemas/schemas/draft3.json',
        'src/superannotate_schemas/schemas/draft4.json',
        'src/superannotate_schemas/schemas/draft6.json',
        'src/superannotate_schemas/schemas/draft7.json',
    ]
                 )
                ],
    include_package_data=True,
    install_requires=[
        "attrs==23.*",
        "pyrsistent==0.*",
        "six==1.*",
        "twisted==23.*"
    ],
    packages=find_packages(where="src"),
    description='SuperAnnotate JSON Schemas',
    author='Vaghinak Basentsyan',
    author_email='vaghinak@superannotate.con',
    url='https://www.superannotate.com/',
    license='MIT',
    description_file="README.md",
)
