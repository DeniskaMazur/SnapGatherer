from launchpad import get_github_url_for_snaps_with_completed_builds
from github import get_plugins, get_scriplets, get_sources, get_snapcraft_yaml_file


plugins = dict()
scriplets = dict()
sources = dict()

def updates_dicts(sfile):
    """
    Updates your snapfile dictianories
    :param sfile: string, containing ur snapfile
    """
    get_scriplets(sfile, scriplets)
    get_sources(sfile, sources)
    get_plugins(sfile, plugins)


if __name__ == "__main__":
    snapfiles = list()

    print("Extracting repository urls")
    urls = get_github_url_for_snaps_with_completed_builds()

    print("Collecting data")
    for url in urls:
        sf = get_snapcraft_yaml_file(url)

        if sf:
            updates_dicts(sf)

    print "Sources:"
    for source, count in sources.items().sort(key=lambda x: x[-1], reverse=True):
        print "{} : {}".format(source, count)

    print "Scriplets:"
    for scriplet, count in scriplets.items().sort(key=lambda x: x[-1], reverse=True):
        print "{} : {}".format(scriplet, count)

    print "Plugins: "
    for plugin, count in plugins.items().sort(key=lambda x: x[-1], reverse=True):
        print "{} : {}".format(plugin, count)