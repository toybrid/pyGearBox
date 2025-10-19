# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
sys.path.insert(0, '../../pyGearBox')

project = 'pyGearBox'
copyright = '2025, Arjun Thekkumadathil'
author = 'Arjun Thekkumadathil'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.napoleon',
    # 'sphinx.ext.viewcode',
]
# autodoc_default_options = {
#     'members': True,
#     'undoc-members': True,
#     'private-members': True,
#     'show-inheritance': True,
# }

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'donate_url': 'https://buymeacoffee.com/cgarjun',
    'github_user': 'toybrid',
    'github_repo': 'pyGearBox',
    'description': 'A powerful, lightweight, and user-friendly plugin manager for Python applications',
    'fixed_sidebar': True,
    'show_relbars': True,
}
