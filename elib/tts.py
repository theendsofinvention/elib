# coding=utf-8
"""
Manages TTS utilities
"""
import calendar
import math
import re
import time
import typing
from pathlib import Path

import gtts
import requests
from gtts import gTTS
from gtts_token.gtts_token import Token

import elib.custom_logging
import elib.path

LOGGER = elib.custom_logging.get_logger('ELIB')


def _patch_faulty_function(self):
    if self.token_key is not None:
        return self.token_key

    timestamp = calendar.timegm(time.gmtime())
    hours = int(math.floor(timestamp / 3600))

    response = requests.get("https://translate.google.com/")
    line = response.text.split('\n')[-1]

    parsed = re.search("(?:TKK='(?:(\d+)\.(\d+))';)", line)
    a, b = parsed.groups()

    result = str(hours) + "." + str(int(a) + int(b))
    self.token_key = result
    return result


# Monkey patch faulty function.
Token._get_token_key = _patch_faulty_function


def text_to_speech(text: str, file_path: typing.Union[str, Path], overwrite: bool = False) -> Path:
    """
    Creates MP3 file from text

    Args:
        text: text to encode
        file_path: path to MP3 file
        overwrite: whether or not to overwrite existing file

    Returns: path to saved MP3

    """
    LOGGER.debug(f'{text}\n->{file_path}')
    file_path = elib.path.ensure_path(file_path, must_exist=False)
    if file_path.exists() and not overwrite:
        LOGGER.error(f'"{file_path}" already exists')
        raise FileExistsError(file_path)
    LOGGER.debug('encoding text')
    tts = gtts.gTTS(text=text)
    LOGGER.debug('saving MP3 file')
    tts.save(str(file_path))
    return file_path
