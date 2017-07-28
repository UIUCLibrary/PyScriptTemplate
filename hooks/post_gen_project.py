import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dirpath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))

if __name__ == "__main__":
    if '{{ cookiecutter.use_pytest }}' != "y":
        remove_dir("tests")

    if '{{ cookiecutter.use_tox }}' != "y":
        remove_file("tox.ini")

    if '{{ cookiecutter.use_sphinx}}' != "y":
        remove_dir("docs")

    if '{{ cookiecutter.use_travis_ci}}' != "y":
        remove_file(".travis")

    if '{{ cookiecutter.use_jenkins_pipeline}}' != "y":
        remove_file("Jenkinsfile")

    if '{{ cookiecutter.create_deployment_yml}}' != "y":
        remove_file("deployment.yml")

    if '{{ cookiecutter.script["add_script"]}}' != "y":
        remove_file("{{ cookiecutter.project_slug }}/__main__.py")
        remove_file("{{ cookiecutter.project_slug }}/cli.py")

