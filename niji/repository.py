"""
Module that contains functions that relates
to handling a repository.
"""

import os
import requests
import tarfile
import json
import re
import semantic_version


class Repository(object):
    """ Class representing a package repository """

    def __init__(self, url, root_dir = ".", cache_dir = ".niji", use_version_folders=False):
        self.url = url
        self.root_dir = root_dir
        self.cache_dir = os.path.join(self.root_dir, cache_dir)
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.use_version_folders = use_version_folders
        self.branchdir = os.path.join(self.cache_dir, branch)
        self.package_list_path = os.path.join(branchdir, "packages.list")


    def get_package_list(self, branch = "main"):
        """
        Fetch or refresh the package list
        for a given branch.
        """
        if not os.path.exists(self.branchdir):
            os.mkdir(self.branchdir)

        # download the package index file
        # and save it to the cache dir
        try:
            with open(self.package_list_path, 'wb') as handle:
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


    def query_package(self, query):
        """
        Retrieve information for a locally installed package
        """
        pass

    def install_packages(self, packages, strict=True):
        """
        Install a set of packages as a unit, making sure that
        there are no resolution conflicts if strict is specified
        """
        installed = []
        if not strict:
            for p in packages:
                installed.extend(self.install_package(p['name'], p['version'], False))


    def install_package(self, package_name, version_spec=None, strict=True):
        """
        Install the package with the specified name

        """
        to_install = {}
        installed = []
        version = self._resolve_version(version_spec)
        package = {"name": package_name, "version": version}
        tree = {}
        with tarfile.TarFile(self.package_list_path, mode="r:gz") as f:
            tree = self._create_install_tree(f, package)

        # actually install the packages


    def _create_install_tree(self, package_dir, package, skip_root=False):

        tree = {}

        if not skip_root:
            tree[package['name']] = {'version': package['version']}

        deps = self._get_dependencies(package_dir, package['name'], package['version'])
        for d in deps:
            n = d['name']
            if not n in tree:
                tree[n] = {"name": n}
                tree[n]['versions'] = []

            entry = tree[n]
            entry['versions'].append(d['version'])

            # resolve version to continue with
                

        return tree
        

    def _get_dependencies(self, package_list, package_name, version):
        fpath = self._get_package_dir(package_name, version)
        fpath = os.path.join(fpath, "{}.npkg".format(package_name))
        dependencies = []
        with package_list.extractfile(fpath) as f:
            package_data = json.load(f)
            dependencies = package_data['dependencies']

        return dependencies


    def _resolve_version(self, package_list, package_name, version_spec=None):
        versions = self._get_versions(package_list, package_name)
        vspec = semantic_version.Spec(version_spec)

        return vspec.select(versions)
        

    def _get_versions(self, package_list, package_name):
        versions = []
        for e in package_list.getnames():
            m = re.search("{}\/(\.+)\/$".format(packate_name), e)
            if m.group[0]:  # is a folder
                versions.append(semantic_version.Version(m.group[0]))

        return versions



    def upload_package(self, package, branch="main"):
        """
        Upload the supplied package to this repository
        and the given branch.
        """
        pass


    def _get_package_dir(self, package_name, version = ""):
        return os.path.join(package_name, version)
