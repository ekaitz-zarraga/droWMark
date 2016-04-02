function! Prueba( blog, user )

    " Get the blog password by user input
    call inputsave()
    let password = input('Enter password: ')
    call inputrestore()
    echo "\n"

    " Prepare arguments for python script.
    python import vim
    python import sys
    python sys.argv = [ vim.eval('a:blog'), vim.eval('a:user'), vim.eval('password'), vim.eval('@%') ]
    " Call script
    exe 'pyfile ' . escape(s:path, ' ') . '/drowmark.py'
    "pyfile drowmark.py

endfunction

let s:path = escape(resolve(expand('<sfile>:p:h')),'\')
