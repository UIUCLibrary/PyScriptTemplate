@echo off

for /f "tokens=1,* delims= " %%a in ("%*") do set EXTRA_ARGS=%%b

if [%1] == []                call:main                  && goto:eof
if "%~1" == "install-dev"    call:install-dev           && goto:eof
{%- if cookiecutter.use_sphinx == "y" %}
if "%~1" == "docs"           call:docs %EXTRA_ARGS%     && goto:eof
{%- endif %}
if "%~1" == "venv"           call:venv                  && goto:eof
if "%~1" == "venvclean"      call:venvclean             && goto:eof
if "%~1" == "test"           call:test                  && goto:eof
if "%~1" == "test-mypy"      call:mypy %EXTRA_ARGS%     && goto:eof
if "%~1" == "build"          call:build                 && goto:eof
if "%~1" == "wheel"          call:wheel                 && goto:eof
if "%~1" == "sdist"          call:sdist                 && goto:eof
{%- if cookiecutter.use_cx_freeze == "y" %}
if "%~1" == "freeze"         call:freeze                && goto:eof
{%- endif %}
{%- if cookiecutter.create_standalone== "y" %}
if "%~1" == "standalone"     call:standalone            && goto:eof
{%- endif %}
if "%~1" == "clean"          call:clean                 && goto:eof
if "%~1" == "help"           call:help                  && goto:eof
if not %ERRORLEVEL% == 0 exit /b %ERRORLEVEL%
goto :error %*

EXIT /B 0

::=============================================================================
:: Display help information about available options
::=============================================================================
:help
    echo Available options:
    echo    make install-dev        Installs the development requirements into active python environment
    echo    make venv               Creates a virtualenv with development requirements
    echo    make venvclean          Removes the generated virtualenv
    echo    make build              Creates a build in the build directory
{%- if cookiecutter.use_sphinx == "y" %}
    echo    make docs               Generates html documentation into the docs/build/html directory
{%- endif %}
    echo    make test               Runs tests
    echo    make test-mypy          Runs MyPy tests
    echo    make wheel              Build a Python built distribution wheel
    echo    make sdist              Build a Python source distribution
{%- if cookiecutter.use_cx_freeze == "y" %}
    echo    make freeze             Build a standalone distribution with CX_Freeze
{%- endif %}
{%- if cookiecutter.create_standalone== "y" %}
    echo    make standalone         Build a standalone distribution
{%- endif %}
    echo    make clean              Removes generated files
goto :eof


::=============================================================================
:: Default target if no options are selected
::=============================================================================
:main
    call:sdist
    call:wheel
    call:docs --build-dir dist/docs
goto :eof


::=============================================================================
:: Install runtime requirements
::=============================================================================
:install-required-deps
    setlocal
    echo Installing runtime requirements
    call venv\Scripts\activate.bat && pip install -r requirements.txt --upgrade-strategy only-if-needed
    endlocal
goto:eof
::=============================================================================
:: Install development requirements
::=============================================================================
:install-dev
    call:venv
    setlocal
    echo Installing development requirements
    call venv\Scripts\activate.bat && pip install -r requirements-dev.txt --upgrade-strategy only-if-needed
    endlocal
goto :eof


::=============================================================================
:: Build a virtualenv sandbox for development
::=============================================================================
:venv
    if exist "venv" echo %CD%\venv folder already exists. To activate virtualenv, use venv\Scripts\activate.bat & goto :eof

    echo Creating a local virtualenv in %CD%\venv
    setlocal

    REM Create a new virtualenv in the venv path
    py -m venv venv
    call :install-required-deps

    endlocal
goto :eof


::=============================================================================
:: Remove virtualenv sandbox
::=============================================================================
:venvclean
    if exist "venv" echo removing venv & RD /S /Q venv
goto :eof


::=============================================================================
:: Build the target
::=============================================================================
:build
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat && python setup.py build
    endlocal
goto :eof

::=============================================================================
:: Create a wheel distribution
::=============================================================================
:wheel
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat && python setup.py bdist_wheel
    endlocal
goto :eof


::=============================================================================
:: Create a source distribution
::=============================================================================
:sdist
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat && python setup.py sdist
    endlocal
goto :eof


{%- if cookiecutter.use_cx_freeze == "y" %}
::=============================================================================
:: Create a cx_freeze distribution
::=============================================================================
:freeze
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat
    python -m pip install -r requirements-freeze.txt
    python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi
    call build\\msi\\{{ cookiecutter.script["cli_command_name"] }}.exe --pytest
    endlocal
goto:eof
{%- endif %}


{%- if cookiecutter.create_standalone== "y" %}
::=============================================================================
:: Create a standalone distribution
::=============================================================================
:standalone
    setlocal
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat
    call windows_build\build_release.bat
    endlocal
goto:eof
{%- endif %}

::=============================================================================
:: Run unit tests
::=============================================================================
:test
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat && python setup.py test
    endlocal
goto :eof


::=============================================================================
:: Test code with mypy
::=============================================================================
:mypy
    call:install-dev
    setlocal
    call venv\Scripts\activate.bat && mypy -p imgvalidator %*
    endlocal
goto :eof

{%- if cookiecutter.use_sphinx == "y" %}
::=============================================================================
:: Build html documentation
::=============================================================================
:docs
    call:install-dev
    echo Creating docs
    setlocal
    call venv\Scripts\activate.bat && python setup.py build_sphinx %*
    endlocal
goto :eof
{%- endif %}

::=============================================================================
:: Clean up any generated files
::=============================================================================
:clean
    setlocal
	call venv\Scripts\activate.bat

	echo Calling cx_setup.py clean
	python cx_setup.py clean --all --quiet

	echo Calling setup.py clean
	python setup.py clean --all --quiet

{%- if cookiecutter.use_sphinx == "y" %}
	echo Cleaning docs
	call docs\make.bat clean
{%- endif %}

	if exist .cache rd /q /s .cache                 && echo Removed .cache
	if exist .reports rd /q /s .reports             && echo Removed .reports
	if exist .mypy_cache rd /q /s .mypy_cache       && echo Removed .mypy_cache
	if exist .eggs rd /q /s .eggs                   && echo Removed .eggs
	if exist .tox rd /q /s .tox                     && echo Removed .tox
	if exist {{ cookiecutter.project_slug }}.egg-info rd /q /s {{ cookiecutter.project_slug }}.egg-info && echo Removed {{ cookiecutter.project_slug }}.egg-info
	endlocal
goto :eof


::=============================================================================
:: If user request an invalid target
::=============================================================================
:error
    echo Unknown option: %*
    call :help
goto :eof
