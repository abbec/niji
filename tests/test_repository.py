import pytest
from niji.repository import Repository
import os

# todo: Mock os

def test_creation(tmpdir):
    repo = Repository("http://localhost:4567", root_dir = str(tmpdir))

    assert os.path.exists(repo.cache_dir)

def test_package_file_fetch(tmpdir):
    repo = Repository("http://localhost:4567", root_dir = str(tmpdir))

    branch = "testbranch"
    repo.get_package_list(branch)

    assert os.path.exists(os.path.join(repo.cache_dir, branch))
