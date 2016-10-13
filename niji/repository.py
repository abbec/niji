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

    def __init__(self, url, branch="main", root_dir = ".", cache_dir = ".niji", use_version_folders=False):
        self.url = url
        self.branch = branch
        self.root_dir = root_dir
        self.cache_dir = os.path.join(self.root_dir, cache_dir)
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        self.use_version_folders = use_version_folders
        self.branchdir = os.path.join(self.cache_dir, self.branch)
        self.package_list_path = os.path.join(self.branchdir, "packages.list")


    def get_package_list(self):
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
                response = requests.get(self.url + "/{0}/packages.list".format(self.branch), stream=True)

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


    def _create_command_list(self, f, package, dl, required_by, deps=None):
            name = package['name']
            spec = package.get('spec', None)
            res_ver = self._resolve_version(f, name, spec)

            if name not in dl:
                dl[name] = []

            dl[name].append((res_ver,
                semantic_version.Spec(spec),
                required_by))

            deps = deps or self._get_dependencies(f, name, res_ver)
            for d in deps:
                self._create_command_list(f, {'name':d['name'], 'spec':d.get('version', None)}, dl, name)


    def create_command_list(self, package=None, package_file=None, strict=False, remove_me_override=None):
        dl = {}
        deps = None

        if package_file:
            deps, package = self._get_dependencies(package_file=package_file)

        with tarfile.open(self.package_list_path, mode="r:gz") as f:
            self._create_command_list(f, package, dl, 'root', deps)

        return dl


    def _get_dependencies(self, package_list=None, package_name=None, version=None, package_file=None):

        package_data = None

        if package_file:
            with open(explicit_file, mode='r') as f:
                package_data = json.load(f)
                dependencies = package_data['dependencies']
        else:
            fpath = self._get_package_dir(package_name, version)
            fpath = os.path.join(fpath, "{}.npkg".format(package_name))
            dependencies = []

            with package_list.extractfile(fpath) as f:
                package_data = json.load(f)
                dependencies = package_data['dependencies']

        return dependencies, package_data


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


    def _get_package_dir(self, package_name, version = ""):
        return os.path.join(package_name, version)
