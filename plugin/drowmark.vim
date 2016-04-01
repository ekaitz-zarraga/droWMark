function! Prueba( blog, user )

    call inputsave()
    let password = input('Enter password: ')
    call inputrestore()
    echo "\n"

    python import vim
    python import sys
    python sys.argv = [ vim.eval('a:blog'), vim.eval('a:user'), vim.eval('password'), vim.eval('@%') ]
    pyfile drowmark.py

endfunction
