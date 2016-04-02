import sys
from wordpress_xmlrpc import Client, WordPressPost
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import StringIO
import io
import pypandoc

# Get arguments from sys.argv, the idea is to
# maintain it simple, making the python file
# callable from outside VIM also.

if not len(sys.argv) == 4:
    print('4 parameters needed:\n\turl username password file')
    raise

url = 'http://' + sys.argv[0] + '/xmlrpc.php'
username = sys.argv[1]
password = sys.argv[2]
postfile = sys.argv[3]


# Files are Markdown + INI mixed, INI is put
# on the top of the file just for adding some
# metadata, the separator is an horizontal ruler

postconfig = ''
postcontent = ''

inheader = True
f = open(postfile, 'r')
for line in f:
    if inheader:
        # FIXME Improve this check
        if line.strip() == '---':
            inheader = False
            continue
        postconfig += line
        continue
    if not inheader:
        postcontent += line
        continue
f.close()

# TODO Parse the INI part

# buf = StringIO.StringIO(postconfig)
# config = ConfigParser.ConfigParser()
# config.readfp(buf)
#     # TODO define the format for the metadata!
# terms_names = {}


# TODO take markdown, convert to HTML and put it
# as post content
postcontent = pypandoc.convert( postcontent, format='md', to='html')
print postcontent #GOOD LOOKING BABY!


# Wordpress related, the content is prepared and the config is read
# wp = Client( url, username, password )
# post = WordPressPost()

