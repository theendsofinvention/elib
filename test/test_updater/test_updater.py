# coding=utf-8

import subprocess
from pathlib import Path

import pytest
from mockito import verifyStubbedInvocationsAreUsed, when

from elib.updater import _github as github, _updater as updater


@pytest.fixture(name='release')
def _release():
    json = {
        'tag_name': '0.3.0',
        'body': 'body',
        'assets': [
            {
                'name': 'dummy',
                'browser_download_url': 'url',
                'size': 10,
                'state': 'state',
            },
            {
                'name': 'asset.exe',
                'browser_download_url': 'url',
                'size': 10,
                'state': 'state',
            },
            {
                'name': 'asset.exe.md5',
                'browser_download_url': 'url',
                'size': 10,
                'state': 'state',
            },
        ]

    }
    yield updater.Release(json)


@pytest.fixture(autouse=True)
def clean_up():
    yield
    bat = Path('update.bat').absolute()
    vbs = Path('update.vbs').absolute()
    for path in (bat, vbs):
        if path.exists():
            path.unlink()


def test_updater(release):
    repo = 'owner/repo'
    current_version = '0.0.1'
    exe = Path('local.exe')
    upd = updater.Updater(repo, current_version, exe)
    when(updater).get_latest_release(repo).thenReturn(release)
    # when(updater.Updater)._download_latest_release().thenReturn(True)
    when(github.Asset).download(...).thenReturn(True)
    when(subprocess).Popen(...)
    with pytest.raises(SystemExit):
        upd.update()
    verifyStubbedInvocationsAreUsed()


def test_updater_no_asset(release, caplog):
    release._json['assets'] = []
    repo = 'owner/repo'
    current_version = '0.0.1'
    exe = Path('local.exe')
    upd = updater.Updater(repo, current_version, exe)
    when(updater).get_latest_release(repo).thenReturn(release)
    upd.update()
    assert 'no executable asset found' in caplog.text
    verifyStubbedInvocationsAreUsed()


def test_updater_up_to_date(release, caplog):
    repo = 'owner/repo'
    current_version = '0.4.0'
    exe = Path('local.exe')
    upd = updater.Updater(repo, current_version, exe)
    when(updater).get_latest_release(repo).thenReturn(release)
    upd.update()
    assert 'already up-to-date' in caplog.text
    verifyStubbedInvocationsAreUsed()


def test_updater_no_release(caplog):
    repo = 'owner/repo'
    current_version = '0.0.1'
    exe = Path('local.exe')
    upd = updater.Updater(repo, current_version, exe)
    when(updater).get_latest_release(repo).thenReturn(None)
    upd.update()
    assert 'unable to obtain a release from Github' in caplog.text
    verifyStubbedInvocationsAreUsed()
