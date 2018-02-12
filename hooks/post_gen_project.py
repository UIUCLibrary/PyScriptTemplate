import contextlib
import os
import shutil
import uuid
import sys
import io
from cookiecutter.main import cookiecutter
import sphinx.quickstart

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

SPHINX_SUFFIX = ".rst"
SPHINX_MASTER = "index"


def generate_docs():
    _run_sphinx_quickstart()


def _run_sphinx_quickstart():
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(sys.stderr):
            sphinx.quickstart.main(argv=[
                "",
                "--sep",
                "--dot=_",
                f'--project={{ cookiecutter.project_slug }}',
                f"--author={{ cookiecutter.author }}",
                f"-v={{ cookiecutter.version }}",
                f"--release={{ cookiecutter.version }}',",
                "--language=en",
                f"--suffix={SPHINX_SUFFIX}",
                f"--master={SPHINX_MASTER}",
                "--epub",
                "--ext-autodoc",
                "--ext-doctest",
                "--ext-githubpages",
                '--templatedir=quickstart',
                "-q",
                "docs",

            ])
    except Exception:
        print(f.getvalue())
        raise


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dirpath):
    file = os.path.join(PROJECT_DIRECTORY, dirpath)
    print(file)
    shutil.rmtree(file)


def create_guid():
    return str(uuid.uuid1()).upper()


def build_guid():
    print("writing guid file")
    with open("UPGRADE_GUID", "w") as f:
        f.write("{}\n".format(create_guid()))


def build_standalone():
    cookiecutter(
        template="https://github.com/UIUCLibrary/PyMSITemplate.git",
        no_input=True,
        output_dir=os.path.join(PROJECT_DIRECTORY, ".."),
        overwrite_if_exists=True,
        extra_context={
            "project_name": "{{ cookiecutter.project_name }}",
            "project_slug": "{{ cookiecutter.project_slug }}",
            "include_docs": "y",
            "description": "{{ cookiecutter.description }}",
            "license_file": "LICENSE",
            "module_name": '{{ cookiecutter.project_slug }}',
            "GUIDs": {
                "upgrade_code": create_guid(),
                "shortcut": create_guid(),
                "project_code": create_guid(),
            }

        }
    )


if __name__ == "__main__":
    if '{{ cookiecutter.use_pytest }}' != "y":
        remove_dir("tests")

    if '{{ cookiecutter.use_tox }}' != "y":
        remove_file("tox.ini")

    if '{{ cookiecutter.use_sphinx}}' == "y":
        # remove_dir("docs")
        generate_docs()

    if '{{ cookiecutter.use_travis_ci}}' != "y":
        remove_file(".travis.yml")

    if '{{ cookiecutter.use_jenkins_pipeline}}' != "y":
        remove_file("Jenkinsfile")

    if '{{ cookiecutter.create_deployment_yml}}' != "y":
        remove_file("deployment.yml")

    if '{{ cookiecutter.script["add_script"]}}' != "y":
        remove_file("{{ cookiecutter.project_slug }}/__main__.py")
        remove_file("{{ cookiecutter.project_slug }}/cli.py")

    if "{{cookiecutter.use_cx_freeze}}".lower() == "y":
        build_guid()
    else:
        remove_file("cx_setup.py")
        remove_file("documentation.url")
        remove_file("requirements-freeze.txt")

    if "{{ cookiecutter.create_standalone }}".lower() == "y":
        build_standalone()
