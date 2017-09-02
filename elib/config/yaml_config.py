# coding=utf-8
"""
Manages ESST configuration
"""

import os

import everett
import everett.manager
import yaml

import collections


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.MutableMapping):
            r = update_nested_dict(d.get(k, {}), v)
            d[k.upper()] = r
        else:
            d[k.upper()] = u[k]
    return d


def flatten_dict(d: collections.MutableMapping, parent_key='', sep='_') -> dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class YAMLConfig:
    def __init__(self, possible_paths):
        self.cfg = {}
        possible_paths = everett.manager.listify(possible_paths)

        for path in possible_paths:
            if not path:
                continue

            path = os.path.abspath(os.path.expanduser(path.strip()))
            if path and os.path.isfile(path):
                self.cfg = update_nested_dict(self.cfg, self.parse_yaml_file(path))

        self.cfg = flatten_dict(self.cfg)

    @staticmethod
    def parse_yaml_file(path: str):
        with open(path) as stream:
            return yaml.load(stream)

    def get(self, key, namespace=None):
        value = everett.manager.get_key_from_envs(self.cfg, key, namespace)
        if value is everett.NO_VALUE:
            return value
        else:
            if isinstance(value, bool):
                return str(value)
            return value
