# coding=utf-8

from pathlib import Path

import pytest


def test_stash(repo, caplog):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    assert 'stashing changes' in caplog.text
    assert not repo.changed_files()


def test_unstash(repo, caplog):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    assert 'stashing changes' in caplog.text
    assert not repo.changed_files()
    repo.unstash()
    assert 'popping stash' in caplog.text
    assert 'test' in repo.changed_files()


def test_unstash_no_stash(repo, caplog):
    repo.unstash()
    assert 'no stash' in caplog.text


def test_stash_no_changes(repo, caplog):
    repo.stash('test')
    assert 'no changes to stash' in caplog.text


def test_stash_untracked_files(repo, caplog):
    Path('test').touch()
    with pytest.raises(SystemExit):
        repo.stash('test')
    assert 'cannot stash; there are untracked files' in caplog.text


def test_stash_modified_index(repo, caplog):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    repo.stage_all()
    with pytest.raises(SystemExit):
        repo.stash('test')
    assert 'cannot stash; index is not empty' in caplog.text


def test_already_stashed(repo, caplog):
    repo.stashed = True
    with pytest.raises(SystemExit):
        repo.stash('test')
    assert 'already stashed' in caplog.text
