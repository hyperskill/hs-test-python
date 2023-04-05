import pkg_resources


def get_installed_version():
    library_name = "hs-test-python"
    installed_library_version = pkg_resources.get_distribution(library_name).version

    return installed_library_version
