#!/bin/sh -e
#
# File: scripts/install-tcz.sh
# Purpose: install tcz packages (using the install_tcz common method)
#

cd $(dirname "$0"); . ./common.sh; cd ..

install_tcz $@

# eof
