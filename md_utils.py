"""
Utils for markdown -> html conversion.
"""

import markdown  # https://python-markdown.github.io

import logging
logger = logging.getLogger('deploy_scripts')

def html(text_md):
    if not isinstance(text_md, str):               # list of strings
        logger.debug(f'LIST {text_md}')
        text_md = ''.join(text_md)
    return markdown.markdown(
        text_md,
    #    extensions=['extra', 'codehilite'],
        extensions=['extra'],
    #    output_format="html5"
    )
