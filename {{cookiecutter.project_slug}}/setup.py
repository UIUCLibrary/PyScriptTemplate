from setuptools import setup
import {{cookiecutter.project_slug}}

with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name={{cookiecutter.project_slug}}.__title__,
    version={{cookiecutter.project_slug}}.__version__,
    packages=['{{cookiecutter.project_slug}}'],
    url={{cookiecutter.project_slug}}.__url__,
    license='University of Illinois/NCSA Open Source License',
    author={{cookiecutter.project_slug}}.__author__,
    author_email={{cookiecutter.project_slug}}.__author_email__,
    description={{cookiecutter.project_slug}}.__description__,
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
)
