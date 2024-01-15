# -*- coding: utf-8 -*-

import typing as T
import sys
import subprocess
import dataclasses

import fire
from pathlib_mate import Path

from ._version import __version__
from .vendor.jsonutils import json_loads
from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectOpsConfig:
    """
    ``pyproject_ops.json`` file stores the configuration for ``pyproject_ops`` CLI
    for your project.

    If you don't want to use the CLI, instead you want to use pyproject_ops
    as a Python library in your own automation script, you can create the
    :class:`PyProjectOps` object yourself.
    """

    package_name: str = dataclasses.field()
    dev_py_ver_major: int = dataclasses.field()
    dev_py_ver_minor: int = dataclasses.field()
    dev_py_ver_micro: int = dataclasses.field()
    doc_host_aws_profile: T.Optional[str] = dataclasses.field(default=None)
    doc_host_s3_bucket: T.Optional[str] = dataclasses.field(default=None)
    doc_host_s3_prefix: T.Optional[str] = dataclasses.field(default="projects/")


def find_pyproject_ops_json(dir_cwd: Path) -> Path:
    """
    Try to locate the ``pyproject_ops.json`` file by searching all the way up.
    """
    if dir_cwd.parent == dir_cwd:
        raise FileNotFoundError(
            f"Cannot find 'pyproject_ops.json' in {dir_cwd} or its parent directory."
        )
    path = dir_cwd.joinpath("pyproject_ops.json")
    if path.exists():
        return path
    else:
        return find_pyproject_ops_json(dir_cwd.parent)


dir_cwd = Path.cwd()
path_pyproject_ops_json = find_pyproject_ops_json(dir_cwd)
pyops_config = PyProjectOpsConfig(
    **json_loads(path_pyproject_ops_json.read_text(encoding="utf-8"))
)
pyops = PyProjectOps(
    dir_project_root=path_pyproject_ops_json.parent,
    package_name=pyops_config.package_name,
    python_version=f"{pyops_config.dev_py_ver_major}.{pyops_config.dev_py_ver_minor}",
)


class Command:
    """
    python project ops command line interface.
    """

    def __call__(
        self,
        version: bool = False,
    ):
        if version:
            print(__version__)
        else:
            path_pyops = Path(sys.executable).parent.joinpath("pyops")
            subprocess.run([f"{path_pyops}", "--help"], check=True)

    def venv_create(self, dry_run: bool = False):
        """
        ** 🐍 Create Virtual Environment
        """
        pyops.create_virtualenv(dry_run=dry_run)

    def venv_remove(self, dry_run: bool = False):
        """
        ** 🗑 🐍 Remove Virtual Environment
        """
        pyops.remove_virtualenv(dry_run=dry_run)

    def install(self, dry_run: bool = False):
        """
        ** 💾 Install main dependencies and Package itself
        """
        pyops.pip_install(dry_run=dry_run)

    def install_dev(self, dry_run: bool = False):
        """
        💾 💻 Install Development Dependencies
        """
        pyops.pip_install_dev(dry_run=dry_run)

    def install_test(self, dry_run: bool = False):
        """
        💾 🧪 Install Test Dependencies
        """
        pyops.pip_install_test(dry_run=dry_run)

    def install_doc(self, dry_run: bool = False):
        """
        💾 📔 Install Document Dependencies
        """
        pyops.pip_install_doc(dry_run=dry_run)

    def install_automation(self, dry_run: bool = False):
        """
        💾 🤖 Install Dependencies for Automation Script
        """
        pyops.pip_install_automation(dry_run=dry_run)

    def install_all(self, dry_run: bool = False):
        """
        ** 💾 💻 🧪 📔 🤖 Install All Dependencies
        """
        pyops.pip_install_all(dry_run=dry_run)

    def poetry_export(self, dry_run: bool = False):
        """
        Export requirements-*.txt from poetry.lock file
        """
        pyops.poetry_export(dry_run=dry_run)

    def poetry_lock(self, dry_run: bool = False):
        """
        ** Resolve dependencies using poetry, update poetry.lock file
        """
        pyops.poetry_lock(dry_run=dry_run)

    def test(self, dry_run: bool = False):
        """
        ** 🧪 Run test
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_test(dry_run=dry_run)
        pyops.run_unit_test(dry_run=dry_run)

    def test_only(self, dry_run: bool = False):
        """
        🧪 Run test without checking test dependencies
        """
        pyops.run_unit_test(dry_run=dry_run)

    def cov(self, dry_run: bool = False):
        """
        ** 🧪 Run code coverage test
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_test(dry_run=dry_run)
        pyops.run_cov_test(dry_run=dry_run)

    def cov_only(self, dry_run: bool = False):
        """
        🧪 Run code coverage test without checking test dependencies
        """
        pyops.run_cov_test(dry_run=dry_run)

    def view_cov(self, dry_run: bool = False):
        """
        👀 🧪 View coverage test output html file locally in web browser.
        """
        pyops.view_cov(dry_run=dry_run)

    def int(self, dry_run: bool = False):
        """
        ** 🧪 Run integration test
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_test(dry_run=dry_run)
        pyops.run_int_test(dry_run=dry_run)

    def int_only(self, dry_run: bool = False):
        """
        🧪 Run integration test without checking test dependencies
        """
        pyops.run_int_test(dry_run=dry_run)

    def build_doc(self, dry_run: bool = False):
        """
        ** 📔 Build documentation website locally
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_doc(dry_run=dry_run)
        pyops.build_doc(dry_run=dry_run)

    def build_doc_only(self, dry_run: bool = False):
        """
        📔 Build documentation website locally without checking doc dependencies
        """
        pyops.build_doc(dry_run=dry_run)

    def view_doc(self, dry_run: bool = False):
        """
        ** 👀 📔 View documentation website locally
        """
        pyops.view_doc(dry_run=dry_run)

    def deploy_versioned_doc(self, dry_run: bool = False):
        """
        🚀 📔 Deploy Documentation Site To S3 as Versioned Doc
        """
        pyops.deploy_versioned_doc(
            bucket=pyops_config.doc_host_s3_bucket,
            prefix=pyops_config.doc_host_s3_prefix,
            aws_profile=pyops_config.doc_host_aws_profile,
            dry_run=dry_run,
        )

    def deploy_latest_doc(self, dry_run: bool = False):
        """
        🚀 📔 Deploy Documentation Site To S3 as Latest Doc
        """
        pyops.deploy_latest_doc(
            bucket=pyops_config.doc_host_s3_bucket,
            prefix=pyops_config.doc_host_s3_prefix,
            aws_profile=pyops_config.doc_host_aws_profile,
            dry_run=dry_run,
        )

    def view_latest_doc(self, dry_run: bool = False):
        """
        👀 📔 View the latest documentation website on S3
        """
        pyops.view_latest_doc(
            bucket=pyops_config.doc_host_s3_bucket,
            prefix=pyops_config.doc_host_s3_prefix,
            dry_run=dry_run,
        )

    def build(self, dry_run: bool = False):
        """
        🏗 Build distribution package locally
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_dev(dry_run=dry_run)
        pyops.python_build(dry_run=dry_run)

    def publish(self, dry_run: bool = False):
        """
        📦 Publish package to PyPI
        """
        pyops.pip_install(dry_run=dry_run)
        pyops.pip_install_dev(dry_run=dry_run)
        pyops.python_build(dry_run=dry_run)
        pyops.twine_upload(dry_run=dry_run)

    def bump_version(
        self,
        how: str,
        minor_start_from: int = 0,
        micro_start_from: int = 0,
        dry_run: bool = False,
    ):
        """
        🔼 Bump semantic version.

        :param how: patch, minor, major
        :param minor_start_from: start from this minor version if you bump major
        :param micro_start_from: start from this micro version if you bump minor
        """
        kwargs = dict(
            minor_start_from=minor_start_from,
            micro_start_from=micro_start_from,
            dry_run=dry_run,
        )
        if how == "patch":
            kwargs["patch"] = True
        elif how == "minor":
            kwargs["minor"] = True
        elif how == "major":
            kwargs["major"] = True
        else:
            raise ValueError(f"invalid value for how: {how}")
        pyops.bump_version(**kwargs)


def main():
    fire.Fire(Command())
