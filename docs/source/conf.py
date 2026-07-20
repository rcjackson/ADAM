# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ADAM'
copyright = '2025, Robert Jackson, Seongha Park'
author = 'Robert Jackson, Seongha Park'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_gallery.gen_gallery",
    "sphinx_gallery.load_style",
    "sphinx_design",
    "myst_nb",
]

sphinx_gallery_conf = {
    "examples_dirs": "../../examples",
    "gallery_dirs": "source/auto_examples",
}

templates_path = ['_templates']
# Sphinx-Gallery generates a downloadable .ipynb copy of each example
# alongside its .rst page. Without this exclude, myst-nb picks up that
# .ipynb as its own document (same docname as the .rst page), executes it
# independently of the gallery's own execution settings, and shadows the
# .rst page's content and labels.
exclude_patterns = ['source/auto_examples/*.ipynb']
source_suffix = ".rst"
master_doc = "index"
nbsphinx_timeout = 120

intersphinx_mapping = {
    'pyart': ('https://arm-doe.github.io/pyart/', None),
}
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
import adam

# The short X.Y version.
version = adam.__version__
# The full version, including alpha/beta/rc tags.
release = adam.__version__

# Numpy autodoc attributes
numpydoc_show_class_members = True


