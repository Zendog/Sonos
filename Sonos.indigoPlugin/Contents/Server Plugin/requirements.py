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
        logger.info("requirements_check starting ...")
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
        package_names_to_install_or_update_list = list()
        package_pip_commands_to_install_or_update = ""
        for line in lines:
            logger.info(f"Line: {line}")
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
            except KeyError as exception_error:
                if not optional:
                    target = ""
                    if requirements_package == "lxml":
                        target = f" --target \"{plugin_packages_folder}\""  # Temporary fix for Indigo IPH lxml issue (12-July-2023)
                    package_names_to_install_or_update_list.append(requirements_package)
                    package_pip_commands_to_install_or_update = f"{package_pip_commands_to_install_or_update}{pip_version} install {requirements_package}=={version.parse(requirements_version)}{target}\n"

                    # results = (f"{results}\n\n'{requirements_package}' package is not installed. Correct this by running the following command in a Terminal window:"
                    #            f"\n========> {pip_version} install {requirements_package}=={version.parse(requirements_version)}{target} <========\n")
                    continue
                else:
                    if requirements_package not in optional_packages_checked:
                        optionals = (f"{optionals}\nOptional '{requirements_package}' Package is missing.\n\n"
                                     "If you need it, copy and paste the following pip command into a terminal window and press return:\n\n"
                                     f"{pip_version} install {requirements_package}=={version.parse(requirements_version)}\n")
                        optional_packages_checked.append(requirements_package)
                    continue

            if version.parse(plugin_package_version) < version.parse(requirements_version):  # noqa
                target = ""
                if requirements_package == "lxml":
                    target = f" --target \"{plugin_packages_folder}\""  # Temporary fix for Indigo IPH lxml issue (12-July-2023)
                package_names_to_install_or_update_list.append(requirements_package)
                package_pip_commands_to_install_or_update = f"{package_pip_commands_to_install_or_update}{pip_version} install --upgrade {requirements_package}=={version.parse(requirements_version)}{target}\n"

                # results = (f"\n{results}\n'{requirements_package}' (version {version.parse(plugin_package_version)}) Package should be updated to version: {version.parse(requirements_version)}."
                #            f"\nRun in a Terminal window: ========> {pip_version} install --upgrade {requirements_package}=={version.parse(requirements_version)}{target} <========\n")

        if len(package_names_to_install_or_update_list) > 0:
            if len(package_names_to_install_or_update_list) == 1:
                pip_message = f"The '{package_names_to_install_or_update_list[0]}' package needs to be installed or updated."
                command_ui = "command"
            else:
                package_names = ""
                for package_name in package_names_to_install_or_update_list:
                    if package_names == "":
                        package_names = f"'{package_name}'"
                    else:
                        if package_name == package_names_to_install_or_update_list[len(package_names_to_install_or_update_list)-1]:
                            package_names = f"{package_names} and '{package_name}'"
                        else:
                            package_names = f"{package_names}, '{package_name}'"
                pip_message = f"The {package_names} packages need to be installed or updated."
                command_ui = "commands"
            pip_message = f"{pip_message}\n\nCopy and paste the following pip {command_ui} into a terminal window and press return:\n"
            pip_message = f"{pip_message}\n{package_pip_commands_to_install_or_update}"
            pip_message = f"\n\n{pip_message}\n\nOnce installed | updated, reload the Plugin. \n\n"
            raise ImportError(False, pip_message)  # False = Normal import error and plugin will be stopped

        if optionals != "":
            optional_warning = f"\n{optionals}\nOnce any of the optional package(s) listed above have been installed, reload the Plugin. \n"
            raise ImportError(True, optional_warning)  # True = Optional import error for which a warning will be issued i.e. plugin won't be stopped

        logger.info("... requirements_check ending.")

    except IOError as exception_message:
        raise IOError(f"Unable to access requirements file to check required packages. IO Error: {exception_message}")
