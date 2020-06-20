"
"
" Plugins
"

" install vim-plug if not found
" https://jordaneldredge.com/blog/why-i-switched-from-vundle-to-plug/
if empty(glob("~/.vim/autoload/plug.vim"))
    execute '!curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
endif

" load plugins
" (on first load of vim, run :PlugInstall to
" get these installed.)
call plug#begin('.vim/plugged')
  Plug 'junegunn/vim-easy-align'
  Plug 'scrooloose/nerdtree'
call plug#end()

" config nerd tree
autocmd vimenter * NERDTree


"
"
" General tweaks
"

" Line Numbers
"     To disable when inside VIM, try :nonumber
set numberwidth=5
set number

colorscheme slate
hi LineNr ctermfg=white ctermbg=darkgray

syntax on


"
"
" Python
"
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4
set autoindent
