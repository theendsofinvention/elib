# coding=utf-8
"""
Manages TTS utilities
"""
import typing
from pathlib import Path

import gtts

from elib import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)


def text_to_speech(text: str, file_path: typing.Union[str, Path], overwrite: False) -> Path:
    """
    Creates MP3 file from text

    :param text: text to encode
    :return: location of MP3
    """
    LOGGER.debug(f'{text}\n->{file_path}')
    if isinstance(file_path, str):
        LOGGER.debug('converting file path to Path')
        file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        LOGGER.error(f'"{file_path}" already exists')
        raise FileExistsError(file_path)
    LOGGER.debug('encoding text')
    tts = gtts.gTTS(text=text, lang='en', slow=True)
    LOGGER.debug('saving MP3 file')
    tts.save(str(file_path))
    return file_path
