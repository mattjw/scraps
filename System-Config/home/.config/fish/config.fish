#
#
# Homebrew
#

# fix: Warning: Homebrew's sbin was not found in your PATH
# note that this is also already in `/etc/paths`
export PATH="/usr/local/sbin:$PATH"

#
#
# Python setup
#

status --is-interactive; and source (pyenv init -|psub)
    # ^ also sets up PATH to include ~/.pyenv/shims 

#
#
# Support for GIT_ROOT
#

source $HOME/.config/fish/functions/set-git-root.fish
