import pytest
import os
import unittest.mock
import semantic_version
import niji.repository as repo

def create_repo(mock_path, exists=True):
    mock_path.exists.return_value = exists
    return repo.Repository("http://localhost:4567")

@unittest.mock.patch('niji.repository.os.path')
@unittest.mock.patch('niji.repository.os')
def test_creation(mock_os, mock_path):
    create_repo(mock_path, exists=False)

    assert mock_os.mkdir.called

def test_package_file_fetch():
    pass

@unittest.mock.patch('niji.repository.json')
@unittest.mock.patch('niji.repository.tarfile')
@unittest.mock.patch('niji.repository.os.path')
def test_create_command_list(mock_path, mock_tarfile, mock_json):
    r = create_repo(mock_path)

    def js(fpath):
        return {}

    mock_json.load = js
    mocktar = unittest.mock.MagicMock()
    mocktar.getnames.return_value = ["Sune/1.0.0/", "Sune/", "Sune/1.1.0/"]
    mocktar.extractfile().__enter__.return_value = "test"
    mock_tarfile.open().__enter__.return_value = mocktar
    cl = r.create_command_list(package={"name": "Sune"})


    # assert something on cl
    assert "Sune" in cl
    assert isinstance(cl['Sune'], list)
    l = cl['Sune']
    assert len(l) == 1
    entry = l[0]
    assert entry[0] == semantic_version.Version("1.1.0")

    
