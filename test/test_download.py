# coding=utf-8
from pathlib import Path

import requests
from elib import download
from elib.downloader import Downloader
from mockito import mock, verify, when

URL = r'http://www.ovh.net/files/1Mio.dat'


def test_download():
    assert download(url=URL, outfile='./test', hexdigest='6cb91af4ed4c60c11613b75cd1fc6116')
    assert Path('./test').exists()


def test_download_wrong_digest():
    assert not download(url=URL, outfile='./test', hexdigest='nope')
    assert not Path('./test').exists()


def test_download_no_digest():
    assert download(url=URL, outfile='./test')
    assert Path('./test').exists()


def test_download_no_data():
    when(Downloader).download_to_memory(...)
    assert not download(url=URL, outfile='./test', hexdigest='6cb91af4ed4c60c11613b75cd1fc6116')
    verify(Downloader).download_to_memory(...)
    assert not Path('./test').exists()


def test_download_to_memory_no_data():
    when(Downloader)._create_response().thenReturn(None)
    assert not download(url=URL, outfile='./test', hexdigest='6cb91af4ed4c60c11613b75cd1fc6116')
    verify(Downloader)._create_response()
    assert not Path('./test').exists()


def test_download_delete_failed():
    Path('./test').touch()
    assert Path('./test').exists()
    when(Downloader)._create_response().thenReturn(None)
    assert not download(url=URL, outfile='./test', hexdigest='6cb91af4ed4c60c11613b75cd1fc6116')
    verify(Downloader)._create_response()
    assert not Path('./test').exists()


def test_download_request_failed():
    req = mock()
    req.ok = False
    req.reason = 'nope'
    when(requests).head(...).thenReturn(req)
    assert not download(url=URL, outfile='./test', hexdigest='6cb91af4ed4c60c11613b75cd1fc6116')
    verify(requests).head(...)
    assert not Path('./test').exists()
