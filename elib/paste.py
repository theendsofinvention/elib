# coding=utf-8
"""
Creates a snippet at glot.io for text sharing
"""

import json
import typing
from collections import namedtuple

import requests

from elib import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)

BASE_URL = 'https://snippets.glot.io/snippets'

PasteContent = namedtuple('PasteContent', 'filename content')


class PasteError(requests.HTTPError):
    pass


def create_new_paste(title, files: typing.List[PasteContent], public: bool = False, language='lua'):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'language': language,
        'title': title,
        'public': public,
        'files': [
            {
                'name': file.filename,
                'content': file.content
            } for file in files
        ],
    }
    req = requests.post(BASE_URL, json=data, headers=headers)
    if req.ok:
        resp = json.loads(req.text)
        url = resp['url'].replace('https://snippets.glot.io', 'https://glot.io')
        return url
    else:
        raise PasteError(f'failed to post content; reason: {req.reason}')

        # response = urlopen(url, data=urlencode(data).encode('ascii')).read()
        # match = re.search(r'href="/raw/(\w+)"', response.decode('utf-8'))
        # if match:
        #     return '%s/show/%s' % (url, match.group(1))
        #
        # if not isinstance(response, str):
        #     response = response.decode()
        # return 'bad response: ' + response
