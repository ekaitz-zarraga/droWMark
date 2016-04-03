import sys
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
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

url = 'https://' + sys.argv[0] + '/xmlrpc.php'
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

# Parse the INI part
buf = StringIO.StringIO(postconfig)
config = ConfigParser()
config.readfp(buf)

terms_names = {}
tags = config.get('wordpress', 'tags')
terms_names['post_tag'] = map(lambda x: x.strip(),tags.split(','))

categories = config.get('wordpress', 'categories')
terms_names['category'] = map(lambda x: x.strip(),categories.split(','))

post_status = config.get('wordpress','status')

title = config.get('wordpress','title')

# Take markdown, convert to HTML and put it as post content
content = pypandoc.convert( postcontent, format='md', to='html' )

# Wordpress related, create the post and the client:
wp = Client( url, username, password )
post = WordPressPost()

post.title = title
post.content = content
post.post_status = post_status
post.terms_names = terms_names
post.id = wp.call(NewPost(post)) # Post it!

print "Posted: " + post.title
print "\nWith Status: " + post.post_status
print "\nAnd ID: " + post.id
