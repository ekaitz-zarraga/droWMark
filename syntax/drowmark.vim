let b:current_syntax = ''
unlet b:current_syntax
syntax include @INI syntax/dosini.vim

syntax region htmlCode start='\[wordpress]$' end="---$"me=s-1 contains=@INI,@Spell

let b:current_syntax = ''
unlet b:current_syntax
syntax include @MD syntax/markdown.vim

syntax region texCode start="---$" end="\%$" contains=@MD,@Spell
