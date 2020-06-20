
function set-git-root -d "Set GIT_ROOT env var with git root dir"
	git status > /dev/null 2>&1
	if test $status = 0
		export GIT_ROOT=(git rev-parse --show-toplevel)
		return
	end

	set -q GIT_ROOT
	if test $status = 0
		set -e GIT_ROOT
	end
end

#
# Bonus function
#
# This func will not be auto-loaded, because
#   https://github.com/jorgebucaran/fish-cookbook#should-function-names-and-file-names-match
# So instead this file should be explicitly source'd
# from `config.fish`

function groot
	cd (git rev-parse --show-toplevel)
end

#
# Event handlers to keep GIT_ROOT updated
#
# This handler will NOT be autoloaded by fish. To work correctly, this
# file should be called from `config.fish`:
#   source $HOME/.config/fish/functions/set-git-root.fish
#
# Inspired by https://brettterpstra.com/2019/10/15/fish-shell-fun-event-handlers/
#
# Uses "--on-event fish_prompt". The fish_prompt event occurs just before
# the prompt appears. The prompt appears when the terminal is opened, and
# after each command is executed. It only applies to interactive terminals
#
# "--on-variable PWD" was also considered, but a PWD changed event is not
# emitted when the terminal first opens

function __set_git_root__handler__on_prompt --on-event fish_prompt
	set-git-root
end
