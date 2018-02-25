# coding=utf-8
from pathlib import Path

import pytest
from git.exc import GitCommandError


def test_tag(repo):
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()
    repo.tag('test')
    assert repo.get_latest_tag() == 'test'
    assert repo.is_on_tag()
    repo.remove_tag('test')
    assert repo.get_latest_tag() is None
    assert not repo.is_on_tag()


def test_get_current_tag(repo):
    assert repo.get_current_tag() is None
    repo.tag('test')
    assert repo.get_current_tag() == 'test'
    Path('test').touch()
    repo.commit('msg')
    assert repo.get_current_tag() is None


def test_existing_tag(repo):
    repo.tag('test')
    Path('test').touch()
    repo.commit('msg')
    assert repo.get_current_tag() is None
    with pytest.raises(GitCommandError):
        repo.tag('test')
    repo.tag('test', overwrite=True)
    assert repo.get_current_tag() == 'test'
