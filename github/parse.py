#!/usr/bin/python2

import requests
import urlparse

import re

_scriplets = ["prepare", "build", "install", "version_script"]
_tar_type_regex = re.compile(r'.*\.((tar(\.(xz|gz|bz2))?)|tgz)$')


def _get_repo_from_url(github_repo_url):
    parsed_url = urlparse.urlparse(github_repo_url)
    return parsed_url.path[1:]


def get_snapcraft_yaml_file(github_repo_url):
    """
    Extracts snapcraft file from reposutory
    :param github_repo_url: string, url of the repository
    :return:
    """

    github_repo = _get_repo_from_url(github_repo_url)
    paths = ['snapcraft.yaml', '.snapcraft.yaml', 'snap/snapcraft.yaml']
    for path in paths:
        url = 'https://raw.githubusercontent.com/{}/master/{}'.format(
            github_repo, path)
        resp = requests.request("GET", url)

        if resp.status_code == 200:
            return resp.text

def get_plugins(snapcraft_file, plugins=None):
    """
    Parse plugins from a snapcraft file
    :param snapcraft_file: string, your snapcraft file
    :param plugins: dict, in case yo want update existing dict
    :return: dict, {plugin: count}
    """
    if plugins == None:
        plugins = {}

    for line in snapcraft_file.split("\n"):
        line = line.strip()
        if line.startswith('plugin: '):
            plugin = line[8:]
            if plugin in plugins:
                plugins[plugin] = plugins[plugin] + 1
            else:
                plugins[plugin] = 1
    return plugins

def get_scriplets(snapcraft_file, scriplets=None):
    """
     Parse scriplets from a snapcraft file
     :param snapcraft_file: string, your snapcraft file
     :param scriplets: dict, in case yo want update existing dict
     :return: dict, {scriplet: count}
     """
    if scriplets == None:
        scriplets = {}

    for line in snapcraft_file.split("\n"):
        line = line.strip()
        line = line.split(":")[0]

        if line in _scriplets:
            if line not in scriplets:
                scriplets[line] = 1
            else:
                scriplets[line] += 1
    return scriplets

def get_sources(snapcraft_file, sources=None):
    """
     Parse sources from a snapcraft file
     :param snapcraft_file: string, your snapcraft file
     :param sources: dict, in case yo want update existing dict
     :return: dict, {source: count}
     """
    if sources == None:
        sources = {}

    for line in snapcraft_file.split("\n"):
        line = line.strip()
        if line.startswith("source:"):
            src_type = _get_source_type_from_uri(line[7:])

            if src_type in sources:
                sources[src_type] += 1
            else:
                sources[src_type] = 1
    return sources

def _get_source_type_from_uri(source):
    """
    Detect source type of source
    Shamelesly stolen from https://github.com/snapcore/snapcraft/tree/master/snapcraft
    :param source: string, your source
    :return: string, source type
    """
    source_type = 'local'
    if source.startswith('bzr:') or source.startswith('lp:'):
        source_type = 'bzr'
    elif source.startswith('git:') or source.startswith('git@') or \
            source.endswith('.git'):
        source_type = 'git'
    elif source.startswith('svn:'):
        source_type = 'subversion'
    elif _tar_type_regex.match(source):
        source_type = 'tar'
    elif source.endswith('.zip'):
        source_type = 'zip'
    elif source.endswith('deb'):
        source_type = 'deb'
    elif source.endswith('rpm'):
        source_type = 'rpm'
    elif source.endswith('7z'):
        source_type = '7z'

    return source_type
