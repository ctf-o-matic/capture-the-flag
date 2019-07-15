on_logout() {
    [ -f "$HISTFILE" ] && rm "$HISTFILE"
    HISTFILE=
}

trap 'on_logout' EXIT
