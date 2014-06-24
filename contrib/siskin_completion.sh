_siskin_task_names()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "$(tasknames)" -- $cur) )
}

complete -F _siskin_task_names taskcat
complete -F _siskin_task_names taskdo
complete -F _siskin_task_names taskless
complete -F _siskin_task_names taskls
complete -F _siskin_task_names taskoutput
complete -F _siskin_task_names taskredo
complete -F _siskin_task_names taskrm
complete -F _siskin_task_names taskwc
