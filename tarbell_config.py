# -*- coding: utf-8 -*-
import markdown as Markdown
import os
import codecs

from flask import Blueprint
from jinja2 import Markup

"""
Tarbell project configuration
"""

# Google spreadsheet key
# CONTEXT_SOURCE_FILE = "_slides.xlsx"
SPREADSHEET_KEY="1tCE9JPtJS8R-ZJLTg5wRuxFu8G7zn5T16Pv1QohCGY8"

# Exclude these files from publication
EXCLUDES = ["*.md", "requirements.txt", "slides/*"]

# Create JSON data at ./data.json, disabled by default
# CREATE_JSON = True

# S3 bucket configuration
S3_BUCKETS = {
    "production": "www.inforight.net/migrahack",
    "staging": "www.inforight.net/migrahack",
}

# Default template variables
DEFAULT_CONTEXT = {
    'name': 'data-workflow',
    'title': 'Access to Public Information in Mexico'
}

blueprint = Blueprint('data_workflow', __name__)


def read_file(path, absolute=False):
    """
    Read the file at `path`. If `absolute` is True, use absolute path,
    otherwise path is assumed to be relative to Tarbell template root dir.
    """
    if not absolute:
        path = os.path.join(os.path.dirname(__file__), path)

    try:
        return codecs.open(path, 'r', 'utf-8').read()
    except IOError:
        return None


@blueprint.app_context_processor
def context_processor():
    """
    Add helper functions to context for all projects.
    """
    return {
        'read_file': read_file,
    }


@blueprint.app_template_filter()
def markdown(value):
    """Run text through markdown process"""
    if value:
        return Markup(Markdown.markdown(value))
    return value
