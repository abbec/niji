import pytest
from niji.repository import Repository
import os

def test_creation(tmpdir):
    repo = Repository("http://localhost:4567", root_dir = str(tmpdir))

    assert os.path.exists(os.path.join(str(tmpdir), repo.cache_dir))
