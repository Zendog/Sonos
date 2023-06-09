#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Requirements Checking © Autolog 2023
#

from packaging import version
import pkg_resources
import sys

# ============================== Custom Imports ===============================
try:
    # noinspection PyUnresolvedReferences
    import indigo
except ImportError:
    pass

# import time  # TODO: REMOVE THIS AS DEBUGGING ONLY


def requirements_check(plugin_id, logger, optional_packages_checked):
    try:
        pip_version = f'pip{sys.version_info.major}.{sys.version_info.minor}'

        # see https://stackoverflow.com/questions/10214827/find-which-version-of-package-is-installed-with-pip
        packages = [dist.project_name for dist in pkg_resources.working_set]
        packages_dict = dict()
        try:
            for count, item in enumerate(packages):
                packages_dict[item] = pkg_resources.get_distribution(item).version
        except:  # noqa
            pass
        plugin_info = indigo.server.getPlugin(plugin_id)
        requirements_path_fn = f"{plugin_info.pluginFolderPath}/Contents/Server Plugin/requirements.txt"

        # Process each package entry in the requirements.txt file
        file = open(requirements_path_fn, 'r')
        lines = file.readlines()
        for line in lines:
            optional = False
            if line == '':  # Ignore if blank line
                continue
            if line[0:1] == "#":  # Ignore if a comment line
                continue

            # Derive requirements_package and requirements_version (allowing for comments)
            requirements_package, rest_of_line = line.split("==")
            rest_of_line_split = rest_of_line.split("#")  # separate on trailing comments (if any)
            requirements_version = rest_of_line_split[0].strip()  # Remove any trailing whitespace

            if "OPTIONAL" in line:
                optional = True

            try:
                plugin_package_version = packages_dict[requirements_package]
            except KeyError as e:
                if not optional:
                    raise ImportError(f"'{requirements_package}' Package missing."
                                      f"\n\n========> Run '{pip_version} install {requirements_package}' in Terminal window, then reload plugin. <========\n")
                else:
                    if requirements_package not in optional_packages_checked:
                        logger.warning(f"'Optional {requirements_package}' Package missing.\n\n"
                                       f"========> If you need it, run '{pip_version} install {requirements_package}' in Terminal window, then reload plugin. <========\n")
                        optional_packages_checked.append(requirements_package)
                    continue

            if version.parse(plugin_package_version) < version.parse(requirements_version):  # noqa
                raise ImportError(f"'{requirements_package}' (version {version.parse(plugin_package_version)}) Package should be updated to version: {version.parse(requirements_version)}."
                                  f"\n\n========> Run '{pip_version} install --upgrade {requirements_package}' in a Terminal window, then reload plugin. <========\n")

    except IOError as exception_message:
        raise IOError(f"Unable to access requirements file to check required packages. IO Error: {exception_message}")
