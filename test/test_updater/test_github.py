# coding=utf-8

import copy
from pathlib import Path

import pytest
import requests
from mockito import mock, verifyStubbedInvocationsAreUsed, when

import elib
from elib.updater import _github as github


@pytest.fixture(name='dummy_asset')
def _dummy_asset():
    return {
        'name': 'name',
        'browser_download_url': 'browser_download_url',
        'size': 10,
        'state': 'state',
    }


@pytest.fixture(name='dummy_release')
def _dummy_release():
    return {
        'tag_name': 'tag_name',
        'body': 'body',
        'assets': []
    }


def test_val(dummy_release):
    release = github.Release(dummy_release)
    assert release.assets == []
    assert isinstance(github.Release.assets, github._Val)


def test_asset(dummy_asset, dummy_release):
    release = github.Release(dummy_release)
    asset = github.Asset(dummy_asset, release)
    for attrib in ['name', 'browser_download_url', 'size', 'state']:
        assert getattr(asset, attrib) == dummy_asset[attrib]


def test_asset_download(dummy_asset, dummy_release):
    release = github.Release(dummy_release)
    asset1 = github.Asset(copy.copy(dummy_asset), release)
    asset2 = github.Asset(copy.copy(dummy_asset), release)
    release._json['assets'] = [asset1, asset2]
    asset1._json['name'] = 'somefile.exe'
    asset2._json['name'] = 'somefile.exe.md5'
    outfile = Path('outfile').absolute()
    when(github.Asset)._get_hexdigest().thenReturn('hexdigest')
    when(github).download('browser_download_url', outfile, hexdigest='hexdigest').thenReturn(True)
    assert asset1.download(outfile)
    verifyStubbedInvocationsAreUsed()


def test_get_hexdigest(dummy_release, dummy_asset):
    release = github.Release(copy.copy(dummy_release))
    asset1 = github.Asset(copy.copy(dummy_asset), release)
    asset2 = github.Asset(copy.copy(dummy_asset), release)
    asset1._json['name'] = 'somefile.exe'
    asset2._json['name'] = 'somefile.exe.md5'
    release._json['assets'] = [asset1._json, asset2._json]
    outfile = Path('outfile').absolute()
    downloader = mock()
    when(downloader).download_to_memory()
    downloader.file_binary_data = 'hexdigest'.encode('utf16')
    when(github).Downloader(...).thenReturn(downloader)
    when(github).download('browser_download_url', outfile, hexdigest='hexdigest').thenReturn(True)
    assert asset1.download(outfile)
    verifyStubbedInvocationsAreUsed()


def test_get_hexdigest_no_md5(dummy_release, dummy_asset):
    release = github.Release(copy.copy(dummy_release))
    asset1 = github.Asset(copy.copy(dummy_asset), release)
    asset1._json['name'] = 'somefile.exe'
    release._json['assets'] = [asset1._json]
    outfile = Path('outfile').absolute()
    when(github).download('browser_download_url', outfile, hexdigest=None).thenReturn(True)
    assert asset1.download(outfile)
    verifyStubbedInvocationsAreUsed()


def test_get_latest_release(dummy_release):
    repo = 'owner/repo'
    req = mock(spec=requests.Request)
    req.ok = True
    when(req).json().thenReturn(dummy_release)
    when(requests).get(rf'https://api.github.com/repos/{repo}/releases/latest', timeout=5).thenReturn(req)
    release = github.get_latest_release(repo)
    assert isinstance(release, github.Release)
    verifyStubbedInvocationsAreUsed()


def test_get_latest_release_req_timeout(caplog):
    repo = 'owner/repo'
    when(requests).get(rf'https://api.github.com/repos/{repo}/releases/latest', timeout=5) \
        .thenRaise(requests.exceptions.Timeout)
    assert github.get_latest_release(repo) is None
    assert 'request timed out' in caplog.text
    verifyStubbedInvocationsAreUsed()


def test_get_latest_release_req_failed(caplog):
    repo = 'owner/repo'
    req = mock(spec=requests.Request)
    req.ok = False
    req.reason = 'testing'
    when(requests).get(rf'https://api.github.com/repos/{repo}/releases/latest', timeout=5).thenReturn(req)
    assert github.get_latest_release(repo) is None
    assert 'request failed: testing' in caplog.text
    verifyStubbedInvocationsAreUsed()
