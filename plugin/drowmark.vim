function! PostWordPress( blog, user )

    " Get the blog password by user input
    echo 'Enter password: '
    let password = s:getPass()


    " Prepare arguments for python script.
    python import vim
    python import sys
    python sys.argv = [ vim.eval('a:blog'), vim.eval('a:user'), vim.eval('password'), vim.eval('@%') ]
    " Call script
    exe 'pyfile ' . escape(s:path, ' ') . '/drowmark.py'
    "pyfile drowmark.py

endfunction

" Get password without showing the echo in the screen
function! s:getPass()
    let password = ""
    let char = nr2char(getchar())

    while char !=  "\<CR>"
        let password = password . char
        let char = nr2char(getchar())
    endwhile
    return password

endfunction

let s:path = escape(resolve(expand('<sfile>:p:h')),'\')
