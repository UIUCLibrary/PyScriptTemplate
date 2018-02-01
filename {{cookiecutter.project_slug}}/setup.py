from setuptools import setup
import os


setup(
    packages=['{{cookiecutter.project_slug}}'],
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
