#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Requirements Checking © Autolog 2023
#

from importlib import metadata
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


def requirements_check(plugin_id, logger, plugin_packages_folder, optional_packages_checked):
    try:
        pip_version = f'pip{sys.version_info.major}.{sys.version_info.minor}'

        # see https://stackoverflow.com/questions/50380624/find-pip-packages-pkg-resources-specify-custom-target-directory
        # see https://stackoverflow.com/questions/10214827/find-which-version-of-package-is-installed-with-pip
        packages = [dist.project_name for dist in pkg_resources.working_set]
        packages_dict = dict()
        try:
            for count, item in enumerate(packages):
                packages_dict[item] = pkg_resources.get_distribution(item).version
        except:  # noqa
            pass

        # Routine to select packages for plugin packages folder
        try:
            # TODO: Derive folder name = DONE
            dists = metadata.distributions(path=[plugin_packages_folder])
            dists_list = list(f"{d.metadata['Name']}=={d.metadata['Version']}" for d in dists)
            for dist in dists_list:
                dist_package, dist_version = dist.split("==")
                packages_dict[dist_package] = dist_version
        except Exception as exception_error:
            a = 1  # Debug point
            pass
        a = 2  # Debug point

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
                    target = ""
                    if requirements_package == "lxml":
                        target = f" --target \"{plugin_packages_folder}\""  # Temporary fix for Indigo IPH lxml issue (12-July-2023)
                    results = (f"{results}\n\n'{requirements_package}' package is not installed. Correct this by running the following command in a Terminal window:"
                               f"\n========> {pip_version} install {requirements_package}{target} <========\n")
                    continue
                else:
                    if requirements_package not in optional_packages_checked:
                        optionals = (f"{optionals}\nOptional '{requirements_package}' Package missing.\n\n"
                                     f"========> If you need it, in a Terminal window: ========> {pip_version} install {requirements_package} <========\n")
                        optional_packages_checked.append(requirements_package)
                    continue

            if version.parse(plugin_package_version) < version.parse(requirements_version):  # noqa
                target = ""
                if requirements_package == "lxml":
                    target = f" --target \"{plugin_packages_folder}\""  # Temporary fix for Indigo IPH lxml issue (12-July-2023)
                results = (f"\n{results}\n'{requirements_package}' (version {version.parse(plugin_package_version)}) Package should be updated to version: {version.parse(requirements_version)}."
                           f"\nRun in a Terminal window: ========> {pip_version} install --upgrade {requirements_package}{target} <========\n")

        if results != "":
            raise ImportError(f"\n{results}\nOnce the package(s) listed above have been installed | updated, reload the Plugin. \n")
        if optionals != "":
            logger.warning(f"\n{optionals}\nOnce any of the optional package(s) listed above have been installed, reload the Plugin. \n")

    except IOError as exception_message:
        raise IOError(f"Unable to access requirements file to check required packages. IO Error: {exception_message}")
