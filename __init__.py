# Standard Library
from StringIO import StringIO

from fabric.api import put, local, run
from fabric.contrib.files import upload_template

from jinja2 import Template

# Local Files
import utilities

# Logging
import logging
logger = logging.getLogger(__name__)


def execute(src, dest, engine=None, context=None, **kwargs):
    """Put a file on the destination server
    """
    context = context or {}
    
    # Choose the engine using a dictionary, to make adding things easier.
    engines = {None: string,
           'raw': raw,
           'jinja2': jinja2}
    
    IOstring = engines[engine](src, context)
    put(IOstring, dest)


# Implementations of various simple formatting engines
def raw(src, context):
    """Render the contents of `src` exactly as wrtten on disk
    Inputs:
        :src: The file to read from
        :context: Unused
    :Output: A StringIO object containing the contents of `src`"""
    new = utilities.resolve(src)
    with open(new) as f:
        return StringIO(f.read())


def string(src, context):
    """Return a StringIO object containing the contents of `src`
    Inputs:
        :src: The text to return
        :context: Unused
    :Output: A StringIO object containing the text"""
    return StringIO(src)


def jinja2(src, context):
    """Return a StringIO object containing the result of rendering the template
    Inputs:
        :src: The template to render
        :context: the context to render the template with  
    :Output: A StringIO object containing the result of rendering the template"""
    
    with open(src, 'r') as f:
        template = Template(f.read())
    return StringIO(template.render(**context))
