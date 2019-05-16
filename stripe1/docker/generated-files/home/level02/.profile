alias l='ls -l'
alias la='ls -la'

clear
test -f motd.txt && cat motd.txt

PS1='\u@\h:\w\$ '
