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
    assert len(cl['Sune']) == 1
    assert str(cl['Sune'][0]['version']) == '1.1.0'


@unittest.mock.patch('niji.repository.json')
@unittest.mock.patch('niji.repository.tarfile')
@unittest.mock.patch('niji.repository.os.path')
def test_create_command_list_dep(mock_path, mock_tarfile, mock_json):
    r = create_repo(mock_path)

    p_jcont_a100 = {
       "name":"pack_a",
       "version":"1.0.0",
       "dependencies": [
          {"name":"pack_c", "spec":"=1.1.1"}
       ]
    }
    p_jcont_a110 = {
       "name":"pack_a",
       "version":"1.1.0",
       "dependencies": [
          {"name":"pack_b", "spec":">=1.0.0"},
          {"name":"pack_c", "spec":"=1.1.1"}
       ]
    }
    p_jcont_b210 = {
       "name":"pack_b",
       "version":"2.1.0",
    }
    p_jcont_b100 = {
       "name":"pack_b",
       "version":"1.0.0",
    }
    p_jcont_c111 = {
       "name":"pack_c",
       "version":"1.1.1",
    }

    j_cont = {'pack_a/1.0.0/pack_a.npkg':p_jcont_a100,
              'pack_a/1.1.0/pack_a.npkg':p_jcont_a110,
              'pack_b/2.1.0/pack_b.npkg':p_jcont_b210,
              'pack_b/1.0.0/pack_b.npkg':p_jcont_b100,
              'pack_c/1.1.1/pack_c.npkg':p_jcont_c111}

    mocktar = unittest.mock.MagicMock()

    def extract_enter(f):
        return mocktar.extractfile.call_args[0][0]

    def json_load(path):
        return j_cont[path]

    def join_path(path_a, path_b):
        return "{}/{}".format(path_a, path_b)

    mock_json.load = json_load

    mocktar.getnames.return_value = ["pack_a/1.0.0/", "pack_a/", "pack_a/1.1.0/",
                                     "pack_b/2.1.0/", "pack_b/", "pack_b/1.0.0/",
                                     "pack_c/1.1.1/", "pack_c/"]

    mocktar.extractfile().__enter__ = extract_enter
    os.path.join = join_path
    mock_tarfile.open().__enter__.return_value = mocktar
    mock_tarfile.open().__exit__.return_value = mocktar
    cl = r.create_command_list(package={"name": "pack_a"})

    assert "pack_a" in cl
    assert len(cl['pack_a']) == 1
    assert str(cl['pack_a'][0]['version']) == '1.1.0'
    assert cl['pack_a'][0]['spec'] == semantic_version.Spec(">0.0.0")
    assert cl['pack_a'][0]['req'] == 'root'

    assert "pack_b" in cl
    assert len(cl['pack_b']) == 1
    assert str(cl['pack_b'][0]['version']) == '2.1.0'
    print("SAUNA "+str(cl['pack_b'][0]['spec']))
    assert cl['pack_b'][0]['spec'] == semantic_version.Spec(">=1.0.0")
    assert cl['pack_b'][0]['req'] == 'pack_a'

    assert "pack_c" in cl
    assert len(cl['pack_c']) == 1
    assert str(cl['pack_c'][0]['version']) == '1.1.1'
    assert cl['pack_c'][0]['spec'] == semantic_version.Spec("=1.1.1")
    assert cl['pack_c'][0]['req'] == 'pack_a'
