# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pyjapi"
copyright = "2022, Jannis Mainczyk"
author = "Jannis Mainczyk"
from pyjapi.cli import __version__

release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.programoutput",  # Dynamically generate script output
    "sphinx_click.ext",  # Generate documentation for click cli
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_git",  # include excerpts from your git history
    # 'sphinx.ext.ifconfig',
    # 'sphinxcontrib.mermaid',
    # 'sphinx_issues',
    # autosummary is required to be explicitly loaded by confluencebuilder
    # (see https://github.com/sphinx-contrib/confluencebuilder/issues/304)
    "sphinx.ext.autosummary",
    "sphinxcontrib.confluencebuilder",
    # Include Markdown Files (README, CHANGELOG, ...)
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

default_role = "py:obj"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_logo = "_static/logo.png"

# include FontAwesome icons
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]

html_theme_options = {
    "footer_icons": [
        {
            "name": "GitLab",
            "url": "https://git01.iis.fhg.de/ks-ip-lib/software/pyjapi",
            "html": "",
            "class": "fa-brands fa-solid fa-gitlab fa-xl",
        },
    ],
}

# -- Options for Confluence Builder ------------------------------------------
# https://sphinxcontrib-confluencebuilder.readthedocs.io/
import os  # read confluence password from env

confluence_publish = True
confluence_server_url = "https://intern.iis.fhg.de/"
confluence_server_user = "mkj"
confluence_server_pass = os.getenv("CONF_PW")
confluence_parent_page = "libjapi Knowledge Base"
confluence_space_name = "DOCS"

# Generic configuration.
confluence_page_hierarchy = True

# Publishing configuration.
confluence_disable_notifications = True
# confluence_purge = True

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://docs.pytest.org/en/latest/", None),
}

# -- Options for sphinx-git --------------------------------------------------
# https://sphinx-git.readthedocs.io/en/latest/using.html

# -- Options for sphinxcontrib-programoutput ---------------------------------
# https://sphinxcontrib-programoutput.readthedocs.io/

# A format string template for the output of the prompt option to command-output. default: '$ {command}\n{output}'
# Available variables: {command} {output} {returncode}
# programoutput_prompt_template = "$ {command}\n{output}"

# -- Options for autodoc -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

# This value selects what content will be inserted into the main body of an autoclass directive.
# The possible values are:
#     "class": Only the class’ docstring is inserted. (default)
#     "init": Only the __init__ method’s docstring is inserted.
#     "both": Both the class’ and the __init__ method’s docstring are concatenated and inserted.
#
autoclass_content = "both"

# This value selects if automatically documented members are:
#     'alphabetical': sorted alphabetical, (default)
#     'groupwise': by member type
#     'bysource': or by source order
# Note that for source order, the module must be a Python module with the source code available.
#
autodoc_member_order = "groupwise"

# The default options for autodoc directives. They are applied to all autodoc directives automatically.
# It must be a dictionary which maps option names to the values. Setting None or True to the value is
# equivalent to giving only the option name to the directives.
#
# The supported options are 'members', 'member-order', 'undoc-members', 'private-members',
# 'special-members', 'inherited-members', 'show-inheritance', 'ignore-module-all' and
# 'exclude-members'.
#
autodoc_default_options = {
    # 'members': None,
    # 'member-order': 'bysource',
    "undoc-members": True,
    "private-members": True,
    # 'special-members': True,
    # 'inherited-members': True,
    "show-inheritance": False,
    "ignore-module-all": True,
    "imported-members": False,
    "exclude-members": None,
}

# This value controls the docstrings inheritance.
#
# True: the docstring for classes or methods, if not explicitly set, is inherited from parents. (default)
# False: docstrings are not inherited.
#
autodoc_inherit_docstrings = True

# -- Options for sphinx-autoapi ----------------------------------------

extensions += ["autoapi.extension"]

autoapi_dirs = ["../../src/pyjapi"]
autoapi_options = [
    "members",
    "undoc-members",
    # "private-members",
    "show-inheritance",
    "show-module-summary",
    # "special-members",
    "imported-members",
]
autoapi_add_toctree_entry = False
