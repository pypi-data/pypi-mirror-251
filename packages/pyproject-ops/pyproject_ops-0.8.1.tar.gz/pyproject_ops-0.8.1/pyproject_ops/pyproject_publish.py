# -*- coding: utf-8 -*-

"""
Publish to Python repository related automation.
"""

import typing as T
import subprocess
import dataclasses
from textwrap import dedent

from .helpers import bump_version, print_command

if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectPublish:
    """
    Namespace class for publishing to Python repository related automation.
    """

    def twine_upload(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Publish to PyPI repository using
        `twine upload <https://twine.readthedocs.io/en/stable/index.html>`_.
        """
        args = [
            f"{self.path_bin_twine}",
            "upload",
            f"{self.dir_dist}/*",
        ]
        with self.dir_project_root.temp_cwd():
            print_command(args)
            if dry_run is False:
                subprocess.run(args, check=True)

    def poetry_publish(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Publish to PyPI repository using
        `poetry publish <https://python-poetry.org/docs/libraries/#publishing-to-pypi>`_.`
        """
        args = [
            f"{self.path_bin_poetry}",
            "publish",
        ]
        with self.dir_project_root.temp_cwd():
            print_command(args)
            if dry_run is False:
                subprocess.run(args, check=True)

    def bump_version(
        self: "PyProjectOps",
        major: bool = False,
        minor: bool = False,
        patch: bool = False,
        minor_start_from: int = 0,
        micro_start_from: int = 0,
        dry_run: bool = False,
    ):
        """
        Bump a semantic version. The current version has to be in x.y.z format,
        where x, y, z are integers.

        :param major: bump major version.
        :param minor: bump minor version.
        :param patch: bump patch version.
        :param minor_start_from: if bumping major version, minor start from this number.
        :param micro_start_from: if bumping minor version, micro start from this number.
        """
        new_version = bump_version(
            current_version=self.package_version,
            major=major,
            minor=minor,
            patch=patch,
            minor_start_from=minor_start_from,
            micro_start_from=micro_start_from,
        )

        # update _version.py file
        version_py_content = dedent(
            """
        __version__ = "{}"
    
        # keep this ``if __name__ == "__main__"``, don't delete!
        # this is used by automation script to detect the project version
        if __name__ == "__main__":  # pragma: no cover
            print(__version__)
        """
        ).strip()
        version_py_content = version_py_content.format(new_version)
        if dry_run is False:
            self.path_version_py.write_text(version_py_content)

        # update pyproject.toml file
        if self.path_pyproject_toml.exists():
            if major:
                action = "major"
            elif minor:
                action = "minor"
            elif patch:
                action = "patch"
            else:  # pragma: no cover
                raise NotImplementedError
            with self.dir_project_root.temp_cwd():
                args = [
                    f"{self.path_bin_poetry}",
                    "version",
                    action,
                ]
                print_command(args)
                if dry_run is False:
                    subprocess.run(args, check=True)
