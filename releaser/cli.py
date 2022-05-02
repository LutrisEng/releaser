#!/usr/bin/env python3

import sys
import click

from releaser.project import Project
from releaser.versions import format_version


@click.group()
def releaser():
    pass


@releaser.command(help="Determine the current version number of this project")
def current_version():
    project = Project()
    version = project.current_version()
    print(format_version(version))


@releaser.command(help="Determine the next version number of this project")
def next_version():
    project = Project()
    version = project.next_version()
    print(format_version(version))


@releaser.command(help="Commit & tag a new release for this project")
def update():
    project = Project()
    version = project.next_version()
    print(f"Version {format_version(version)}")
    print("Writing to RELEASE_NOTES.md")
    project.save_changelog_entry()
    print(f"Committing release {format_version(version)}")
    project.commit_changelog_entry()
    print(f"Tagging {format_version(version)}")
    project.tag_version()
    print("Now, to release this version:")
    print("  git push --tags")


@releaser.command(help="Exits with code zero if this commit is tagged with a valid version number, non-zero otherwise")
def check_tag():
    project = Project()
    version = project.tagged_version()
    if version is not None:
        print(f"Version {format_version(version)}")
        sys.exit(0)
    else:
        print("Not tagged with release")
        sys.exit(1)


if __name__ == '__main__':
    releaser()
