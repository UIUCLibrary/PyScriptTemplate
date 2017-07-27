import sys

{%- if cookiecutter.script["add_script"] == "y" %}
contains_script = True
script_name = '{{ cookiecutter.script["cli_command_name"] }}'
if script_name.strip() == "":
    print("Error: Scripts need a valid cli_command_name")
    sys.exit(1)
{%- endif %}

