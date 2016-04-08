function! PostWordPress()
    call inputsave()
    let l:user = input('Enter username: ')
    call inputrestore()
    echo "\n"

    " Get the blog password by user input
    echo 'Enter password: '
    let l:password = s:getPass()


    " Prepare arguments for python script.
    python import vim
    python import sys
    let l:script = escape(s:path, ' ') . '/drowmark.py'
    python sys.argv = [ vim.eval('l:script'), vim.eval('l:user'), vim.eval('l:password'), vim.eval('@%') ]
    " Call script
    exe 'pyfile ' . l:script
    "pyfile drowmark.py

endfunction

function! NewWordPress()
    let l:template = escape(s:path, ' ') . '/../templates/drowmark.template'
    exec 'read '. l:template
    setlocal ft=drowmark
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

command! NewWordPress call NewWordPress()
command! PostWordPress call PostWordPress()
