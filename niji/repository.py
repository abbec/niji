"""
Module that contains functions that relates
to handling a repository.
"""

import os, requests

class Repository:
    """ Class representing a package repository """

    def __init(self, url, root_dir = ".", cahce_dir = ".niji"):
        self.url = url
        self.cache_dir = cahce_dir
        self.root_dir = root_dir
        if not os.path.exists(os.path.join(self.root_dir, self.cache_dir)):
            os.mkdir(os.path.join(self.root_dir, self.cache_dir))

    def get_package_list(self, branch):
        """
        Fetch or refresh the package list
        for a given branch.
        """
        if not os.path.exists(os.path.join(self.root_dir, self.cache_dir, branch)):
            os.mkdir(os.path.join(self.root_dir, self.cache_dir, branch))

        # download the package index file

    def search_package(self, query):
        """
        Search for a package in this package
        repository. If the package list has
        not been fetched, this will be done first.

        Returns a list of package names that matches the query
        or an empty list if no packages matches the query.
        """
        pass

    def get_diff_packages(self, package_name, version):
        """
        Returns a list of the available diff packages
        for the given package that is newer than the version
        given.
        """

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
