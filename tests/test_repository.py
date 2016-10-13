import pytest
from niji.repository import Repository
import os
import unittest

# todo: Mock os
@unittest.mock.patch('niji.repository.os.path')
@unittest.mock.patch('niji.repository.os')
def test_creation(mock_os, mock_path):
    mock_path.exists.return_value = False
    repo = Repository("http://localhost:4567")

    assert mock_os.mkdir.called

def test_package_file_fetch():
    pass

@unittest.mock.patch('niji.repository.os.path')
def test_create_command_list(mock_path):
    mock_path.exists.return_value = True
    repo = Repository("http://localhost:4567")

    
