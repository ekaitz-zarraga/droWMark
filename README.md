# droWMark

Vim plugin to post from VIM to Wordpress using Markdown.

It uses an special template in files, they are a mix between an INI header and
a MarkDown content. There are some templates in `templates` directory and the
`examples` directory contains some working examples.


## Notes

It keeps python code as separate as possible from VIM. Python code is also
callable from outside with the same functionality. VIM is only an interface to
insert the parameters correctly.

### Useful links

- [How to write vim plugins](http://stevelosh.com/blog/2011/09/writing-vim-plugins/)

- [Python in vim plugins](http://vimdoc.sourceforge.net/htmldoc/if_pyth.html#:pyfile)

- [XML-RPC Wordpress](http://python-wordpress-xmlrpc.readthedocs.org/en/latest/overview.html)

- [Syntastic help file](https://github.com/scrooloose/syntastic/blob/master/doc/syntastic.txt)
