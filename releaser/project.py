from datetime import date
import os
from typing import Iterator, Optional

from git import Commit, Repo
from releaser.io import default_git_actor, prepend

from releaser.versions import Version, format_version, increment_version, parse_version


class Project:
    path: str
    repo: Repo

    def __init__(self, path=os.getcwd()) -> None:
        self.path = path
        self.repo = Repo(path)

    def release_notes_path(self) -> str:
        return os.path.join(self.path, "RELEASE_NOTES.md")

    def current_version(self) -> Optional[Version]:
        try:
            with open(self.release_notes_path(), "r") as f:
                firstline = f.readline().strip().removeprefix("# ")
            return parse_version(firstline)
        except:
            return None

    def next_version(self) -> Version:
        return increment_version(self.current_version())

    def commits_since_current_version(self) -> Iterator[Commit]:
        current_version = self.current_version()
        if current_version is None:
            return self.repo.iter_commits(rev="HEAD")
        else:
            return self.repo.iter_commits(rev=f"{format_version(current_version)}..HEAD")

    def generate_changelog_entry(self, new_version=None):
        if new_version is None:
            new_version = self.next_version()
        changelog = f"# {format_version(new_version)}\n"
        for commit in self.commits_since_current_version():
            message = commit.message.splitlines()[0].strip()
            timestamp_date = date.fromtimestamp(commit.committed_date)
            timestamp = timestamp_date.isoformat()
            changelog += f" - {message} ({timestamp})\n"
        return f"{changelog}\n"

    def save_changelog_entry(self):
        entry = self.generate_changelog_entry()
        prepend(self.release_notes_path(), entry)

    def commit_changelog_entry(self):
        index = self.repo.index
        index.add(self.release_notes_path())
        actor = default_git_actor(self.repo)
        index.commit(f"Release {format_version(self.current_version())}",
                     author=actor, committer=actor)

    def tag_version(self):
        self.repo.create_tag(format_version(self.current_version()))
