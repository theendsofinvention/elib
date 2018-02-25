# coding=utf-8

import os
import subprocess
from pathlib import Path

import mimesis
import pytest

import elib


class _CTX:
    obj = {'dry_run': False}


def pytest_collection_modifyitems(items):
    for item in items:
        if 'test_repo/' in item.nodeid:
            item.add_marker(pytest.mark.long)


@pytest.fixture()
def repo(dummy_git_repo):
    dummy_git_repo.create()
    _repo = elib.repo.Repo()
    yield _repo


@pytest.fixture(params=[[mimesis.File().file_name() for _ in range(5)] for _ in range(1)])
def file_set(request):
    file_set_ = list(map(Path, request.param))
    for file_ in file_set_:
        file_.touch()
    yield file_set_


@pytest.fixture()
def dummy_git_repo():
    null = open(os.devnull, 'w')

    def create():
        subprocess.check_call(('git', 'init'), stdout=null)
        Path('./init').touch()
        subprocess.check_call(('git', 'add', './init'), stdout=null)
        subprocess.check_call(('git', 'commit', '-m', 'init commit'), stdout=null)

    dummy_git_repo.create = create

    yield dummy_git_repo


@pytest.fixture(autouse=True)
def _global_tear_down(tmpdir):
    """
    Maintains a sane environment between tests
    """
    environ = dict(os.environ)
    try:
        del os.environ['APPVEYOR']
    except KeyError:
        pass
    current_dir = os.getcwd()
    folder = Path(tmpdir).absolute()
    os.chdir(folder)
    yield
    os.chdir(current_dir)
    os.environ = environ
