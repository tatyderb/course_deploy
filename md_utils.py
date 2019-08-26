"""
Utils for markdown -> html conversion.
"""

import markdown # https://python-markdown.github.io

def html(text_md):
    if not isinstance(text_md, str):               # list of strings
        print('LIST', text_md)
        text_md = ''.join(text_md)
    return markdown.markdown(
        text_md,
        extensions=['extra', 'codehilite'],
    #    output_format="html5"
    )
