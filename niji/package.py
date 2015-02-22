"""
Package module to represent a package
"""
class Package(object):
    def __init__(self):
        pass

    def install(self):
        """
        Install the package.
        """
        pass

    def remove(self):
        """
        Remove a package by deleting all the
        files that the package claims to have
        installed.
        """
        pass

    def is_installed(self):
        """
        Returns true if the package is installed
        under the current root.
        """
        pass

    def get_version(self):
        """
        Returns the installed version (or None)
        for this package.
        """
        pass

class DiffPackage(Package):
    """
    Class representing a diff package.
    That is a package that is only a diff from
    a given full package. A diff package can be applied
    to a package that is already installed locally.
    """
    pass

def generate_diff_package(original, new):
    return DiffPackage()

def apply_diff_package(original, diff_package):
    pass

def create_from_description_file(filename):
    return Package()

def create_from_description(**kwargs):
    return Package()
