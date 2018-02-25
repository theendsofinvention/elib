# coding=utf-8

from pathlib import Path

import pytest


def test_stash(repo, capsys):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    out, _ = capsys.readouterr()
    assert 'Stashing changes' in out
    assert not repo.changed_files()


def test_unstash(repo, capsys):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    assert 'test' in repo.changed_files()
    repo.stash('test')
    out, _ = capsys.readouterr()
    assert 'Stashing changes' in out
    assert not repo.changed_files()
    repo.unstash()
    out, _ = capsys.readouterr()
    assert 'Popping stash' in out
    assert 'test' in repo.changed_files()


def test_unstash_no_stash(repo, capsys):
    repo.unstash()
    _, err = capsys.readouterr()
    assert 'No stash' in err


def test_stash_no_changes(repo, capsys):
    repo.stash('test')
    out, _ = capsys.readouterr()
    assert 'No changes to stash' in out


def test_stash_untracked_files(repo, capsys):
    Path('test').touch()
    with pytest.raises(SystemExit):
        repo.stash('test')
    _, err = capsys.readouterr()
    assert 'Cannot stash; there are untracked files' in err


def test_stash_modified_index(repo, capsys):
    Path('test').touch()
    repo.commit('test')
    Path('test').write_text('test')
    repo.stage_all()
    with pytest.raises(SystemExit):
        repo.stash('test')
    _, err = capsys.readouterr()
    assert 'Cannot stash; index is not empty' in err


def test_already_stashed(repo, capsys):
    repo.stashed = True
    repo.stash('test')
    _, err = capsys.readouterr()
    assert 'Already stashed' in err