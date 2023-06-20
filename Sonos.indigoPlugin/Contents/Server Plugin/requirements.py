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

        results = ""
        optionals = ""

        # Process each package entry in the requirements.txt file
        file = open(requirements_path_fn, 'r')
        lines = file.readlines()
        for line in lines:
            optional = False
            if line == '':  # Ignore if blank line
                continue
            if line[0:1] == "#" and line[0:10] != "# OPTIONAL":  # Ignore if a comment line and not an optional check
                continue

            # Derive requirements_package and requirements_version (allowing for comments)
            if line[0:10] == "# OPTIONAL":
                optional = True
                line = line[10:].strip()

            # logger.info(f"Line: {line}")  # TODO: Debug only
            requirements_package, requirements_version = line.split("==")

            try:
                plugin_package_version = packages_dict[requirements_package]
            except KeyError as e:
                if not optional:
                    results = (f"\n{results}\n'{requirements_package}' Package missing."
                               f"\n========> Run '{pip_version} install {requirements_package}' in Terminal window. <========\n")
                else:
                    if requirements_package not in optional_packages_checked:
                        optionals = (f"\n{optionals}\nOptional '{requirements_package}' Package missing.\n\n"
                                     f"========> If you need it, run '{pip_version} install {requirements_package}' in Terminal window. <========\n")
                        optional_packages_checked.append(requirements_package)
                    continue

            if version.parse(plugin_package_version) < version.parse(requirements_version):  # noqa
                results = (f"\n{results}\n'{requirements_package}' (version {version.parse(plugin_package_version)}) Package should be updated to version: {version.parse(requirements_version)}."
                           f"\n========> Run '{pip_version} install --upgrade {requirements_package}' in a Terminal window. <========\n")

        if results != "":
            raise ImportError(f"{results}\nOnce package(s) listed above have been installed | updated, reload the Plugin. \n")
        elif optionals != "":
            logger.warning(f"{optionals}\nIf any of the optional package(s) listed above have been installed, reload the Plugin. \n")

    except IOError as exception_message:
        raise IOError(f"Unable to access requirements file to check required packages. IO Error: {exception_message}")
