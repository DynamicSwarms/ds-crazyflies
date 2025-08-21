# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(".."))

project_root = os.path.abspath("../src")

# Recursively add all folders with an __init__.py to sys.path
# This ensures all packages are found
for root, dirs, files in os.walk(project_root):
    if "setup.py" in files:
        sys.path.insert(0, root)


project = "ds-crazyflies"
copyright = f"2024-{datetime.datetime.now().year}, Vinzenz Malke, Sebastian Rossi"
author = "Vinzenz Malke, Sebastian Rossi"
release = "0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_collapse",
    "sphinx_tabs.tabs",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


autodoc_typehints = "description"
autoclass_content = "both"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
}
html_static_path = ["_static"]


# Do not import certain modules to build independently of installation

autodoc_mock_imports = [
    "rclpy",
    "crazyflie_webots_gateway_interfaces",
    "crazyflie_hardware_gateway_interfaces",
    "crazyflies_interfaces",
    "crazyflie_interfaces",
    "builtin_interfaces",
    "std_msgs",
    "geometry_msgs",
]
