#!/usr/bin/python2

import os

from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously(
    'elopio_script', 'production', version='devel')


def get_github_url_for_snaps_with_completed_builds():
    github_snaps = launchpad.snaps.findByURLPrefix(
        url_prefix='https://github.com')
    # TODO there are projects using branches other than master.
    # Ask how to get the branch from launchpad. --elopio - 20170703
    return [
        snap.git_repository_url for snap in github_snaps
        if snap.completed_builds.total_size > 0
    ]
