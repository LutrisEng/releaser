from genericpath import exists
from git import Actor, Repo


def prepend(filename, prepend_content):
    if exists(filename):
        with open(filename, "r+") as f:
            existing_content = f.read()
            f.seek(0, 0)
            f.write(prepend_content + existing_content)
    else:
        with open(filename, "w") as f:
            f.write(prepend_content)


def default_git_actor(repo: Repo) -> Actor:
    reader = repo.config_reader()
    email = reader.get_value("user", "email")
    name = reader.get_value("user", "name")
    return Actor(name, email)
