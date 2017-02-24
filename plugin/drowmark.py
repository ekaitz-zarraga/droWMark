import sys
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from io import StringIO
import codecs
import panflute as pf
from os import path
import mimetypes

WP = None
postfile = ''

def imageURLs(elem, doc):

    if isinstance(elem, pf.Image):
        # Handles paths if they are relative to the post
        here = path.dirname( postfile )
        url = path.join( here, elem.url ) # Make path absolute
        if not path.exists(url):
            return
        mime = mimetypes.guess_type(url, strict = True)[0]
        if not mime.split('/')[0] == 'image':
            # It's not an image!
            return

        res = uploadFile(url, mime)
        elem.url = res['url']
        return elem

def uploadFile( url, mime ):

    data = {}
    data['name'] = path.basename(url)
    data['type'] = mime
    with open(url) as f:
        data['bits'] = xmlrpc_client.Binary(f.read())

    response = WP.call(media.UploadFile(data))
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    return response




# Get arguments from sys.argv, the idea is to
# maintain it simple, making the python file
# callable from outside VIM also.

if not len(sys.argv) == 4:
    print('3 parameters needed:\n\t username password file')
    raise BaseException

username = sys.argv[1]
password = sys.argv[2]
postfile = sys.argv[3]


# Files are Markdown + INI mixed, INI is put
# on the top of the file just for adding some
# metadata, the separator is an horizontal ruler

postconfig = ''
postcontent = ''

inheader = True
f = codecs.open(postfile, 'r', 'utf-8')
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
# TODO add thumbnail
buf = StringIO(postconfig)
config = ConfigParser()
config.readfp(buf)

terms_names = {}
tags = config.get('wordpress', 'tags')
terms_names['post_tag'] = map(lambda x: x.strip(),tags.split(','))

categories = config.get('wordpress', 'categories')
terms_names['category'] = map(lambda x: x.strip(),categories.split(','))

post_status = config.get('wordpress','status')

url = config.get('wordpress','url')
url = 'https://' + url + '/xmlrpc.php'

title = config.get('wordpress','title')

# Wordpress related, create the post
WP = Client( url, username, password )
post = WordPressPost()

# Take markdown, convert to HTML and put it as post content
#content = pypandoc.convert( postcontent, format='md',
#                                         to='html')
postdocument = pf.convert_text(postcontent, input_format='markdown',
                                            output_format='panflute',
                                            standalone=True)

pf.run_filters( [ imageURLs ], doc = postdocument )
content = pf.convert_text(postdocument, input_format='panflute',
                                        output_format='html')


post.title = title
post.content = content
post.post_status = post_status
post.terms_names = terms_names
post.id = WP.call(NewPost(post)) # Post it!

print( "Posted: " + post.title )
print( "\nWith Status: " + post.post_status )
print( "\nAnd ID: " + post.id )
