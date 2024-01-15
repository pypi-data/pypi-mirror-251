.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.8.1 (2023-01-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``pyops build`` command.
- add ``--dry-run`` flag to most of command. if dry run is True, then only print the underlying command to run, but taking no effect.


0.7.2 (2023-12-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add the optional ``prefix`` argument to ``pyproject.api.PyProjectOps.deploy_versioned_doc``, ``pyproject.api.PyProjectOps.deploy_latest_doc``, ``pyproject.api.PyProjectOps.view_latest_doc`` method.
- now the CLI will print help information if you type ``pyops`` without any arguments.
- now the ``pyproject.api.PyProjectOps.from_pyproject_toml()`` method can take a string as input.
- add man page to ``README.rst``


0.7.1 (2023-12-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``pyproject_ops.api.bump_version`` to bump version in ``_version.py`` and ``pyproject.toml``.
- add ``pyops bump-version --how patch`` to bump patch, minor, major version in ``_version.py`` and ``pyproject.toml``.


0.6.3 (2023-12-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix the ``dry_run`` flag in ``pyproject_ops.api.PyProjectOps.view_cov``.


0.6.2 (2023-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix the pypi metadata.


0.6.1 (2023-12-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``dry_run`` parameter to most of the ``pyproject_ops.api.PyProjectOps`` methods, allow user to run them without doing anything, just to see what would happen.


0.5.2 (2023-12-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that ``pyproject_ops.api.PyProjectOps.poetry_export`` calls the wrong method.


0.5.1 (2023-12-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- the following methods now support an optional ``verbose`` parameter, if it is True, then display human friendly log messages to the console.
    - ``pyproject_ops.api.PyProjectOps.create_virtualenv``
    - ``pyproject_ops.api.PyProjectOps.remove_virtualenv``
    - ``pyproject_ops.api.PyProjectOps.pip_install``
    - ``pyproject_ops.api.PyProjectOps.pip_install_dev``
    - ``pyproject_ops.api.PyProjectOps.pip_install_test``
    - ``pyproject_ops.api.PyProjectOps.pip_install_doc``
    - ``pyproject_ops.api.PyProjectOps.pip_install_automation``
    - ``pyproject_ops.api.PyProjectOps.pip_install_all``
    - ``pyproject_ops.api.PyProjectOps.pip_install_awsglue``
    - ``pyproject_ops.api.PyProjectOps.poetry_lock``
    - ``pyproject_ops.api.PyProjectOps.poetry_export``
    - ``pyproject_ops.api.PyProjectOps.poetry_install``
    - ``pyproject_ops.api.PyProjectOps.poetry_install_dev``
    - ``pyproject_ops.api.PyProjectOps.poetry_install_test``
    - ``pyproject_ops.api.PyProjectOps.poetry_install_doc``
    - ``pyproject_ops.api.PyProjectOps.poetry_install_all``
    - ``pyproject_ops.api.PyProjectOps.run_unit_test``
    - ``pyproject_ops.api.PyProjectOps.run_cov_test``
    - ``pyproject_ops.api.PyProjectOps.run_int_test``
    - ``pyproject_ops.api.PyProjectOps.run_load_test``
    - ``pyproject_ops.api.PyProjectOps.python_build``
    - ``pyproject_ops.api.PyProjectOps.poetry_build``
    - ``pyproject_ops.api.PyProjectOps.build_doc``
    - ``pyproject_ops.api.PyProjectOps.view_doc``
    - ``pyproject_ops.api.PyProjectOps.deploy_versioned_doc``
    - ``pyproject_ops.api.PyProjectOps.deploy_latest_doc``


0.4.1 (2023-12-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``from_pyproject_toml`` method.


0.3.1 (2023-07-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add AWS glue related paths. add ``pip_install_awsglue`` command to install ``awsglue`` package.


0.2.3 (2023-07-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add ``dir_lambda_app_vendor_python_lib`` path.


0.2.2 (2023-06-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix a bug that ``pyops publish`` command forget to install dev dependencies.

**Miscellaneous**

- loosen the ``fire`` dependency version requirements to ``>=0.1.3``.


0.2.1 (2023-06-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``pyops view-cov`` command to view coverage test output html file locally in web browser.


0.1.1 (2023-05-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- reimplement all features in `pygitrepo <https://github.com/MacHu-GWU/pygitrepo-project>`_ in ``pyproject_ops``.
- add important paths enum
- add venv management
- add dependencies management
- add test automation
- add documentation build
- add source distribution build
