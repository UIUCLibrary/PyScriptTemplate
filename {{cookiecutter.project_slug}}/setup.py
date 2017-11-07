from setuptools import setup
import os
import {{cookiecutter.project_slug}}

def get_project_metadata():
    metadata_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '{{cookiecutter.project_slug}}', '__version__.py')
    metadata = dict()
    with open(metadata_file, 'r', encoding='utf-8') as f:
        exec(f.read(), metadata)
    return metadata

with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()
metadata = get_project_metadata()

setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    packages=['{{cookiecutter.project_slug}}'],
    url=metadata["__url__"],
    license='University of Illinois/NCSA Open Source License',
    maintainer=metadata["__maintainer__"],
    maintainer_email=metadata["__maintainer_email__"],
    description=metadata["__description__"],
    long_description=readme,
    test_suite="tests",
    {%- if cookiecutter.use_pytest == "y" %}
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    {%- endif %}
	{%- if cookiecutter.script["add_script"] == "y" %}
    entry_points={
         "console_scripts": [
             '{{cookiecutter.script["cli_command_name"]}} = {{cookiecutter.project_slug}}.__main__:main'
         ]
     },
	{%- endif %}
    zip_safe=False,
)
