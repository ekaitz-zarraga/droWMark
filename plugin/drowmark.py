import sys
from wordpress_xmlrpc import Client

# Get arguments from sys.argv, the idea is to
# maintain it simple, making the python file
# callable from outside VIM also.

print sys.argv # Some debugging


# Files are Markdown + INI mixed, INI is put
# on the top of the file just for adding some
# metadata, the separator is an horizontal ruler

# TODO Parse the INI part (maybe YAML?)

# TODO take markdown, convert to HTML and put it
# as post content
