"""
Module that contains functions that relates
to handling a repository.
"""

import os, requests

class Repository:
    """ Class representing a package repository """

    def __init__(self, url, root_dir = ".", cache_dir = ".niji"):
        self.url = url
        self.root_dir = root_dir
        self.cache_dir = os.path.join(self.root_dir, cache_dir)
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def get_package_list(self, branch):
        """
        Fetch or refresh the package list
        for a given branch.
        """
        branchdir = os.path.join(self.cache_dir, branch)
        if not os.path.exists(branchdir):
            os.mkdir(branchdir)

        # download the package index file
        # and save it to the cache dir
        try:
            with open(os.path.join(branchdir, "packages.list"), 'wb') as handle:
                response = requests.get(self.url + "/{0}/packages.list".format(branch), stream=True)

                if not response.ok:
                    # todo: something went wrong
                    print("There was an error in fetching package list")
                    return

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        except requests.ConnectionError:
            print("Error in connecting to {0}.".format(self.url))

    def search_package(self, query):
        """
        Search for a package in this package
        repository. If the package list has
        not been fetched, this will be done first.

        Returns a list of package names that matches the query
        or an empty list if no packages matches the query.
        """
        return [""]

    def get_diff_packages(self, package_name, version):
        """
        Returns a list of the available diff packages
        for the given package that is newer than the version
        given.
        """
        pass

    def download_package(self, package_name):
        """
        Download the package with the specified name.

        Returns a package object that can be used to
        install the package.
        """
        pass

    def upload_package(self, branch, package):
        """
        Upload the supplied package to this repository
        and the given branch.
        """
        pass

    def clear_cache(self, delete_have = False):
        """
        Clear the cache by deleting downloaded packages
        and the package list. If delete_have is true,
        the have file will be deleted and niji will
        think that no packages are installed under
        this root.
        """
        pass
