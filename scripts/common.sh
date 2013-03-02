#!/bin/sh
#
# File: common.sh
# Purpose: common configuration and shell functions
#

# tiny core related
iso_url=http://distro.ibiblio.org/tinycorelinux/4.x/x86/release/Core-current.iso
tcz_url=http://distro.ibiblio.org/tinycorelinux/4.x/x86/tcz
tcz_dir=./tcz

# internally used dirs and paths
livecd0=./livecd.iso
livecd1=./remastered.iso
mnt=./mnt
extract=./extract
newiso=./newiso
squashfs=$newiso/boot/core.gz

# ctf1 related
ctf1=./ctf1
ctf1_orig=$ctf1/orig
ctf1_append=$ctf1/append
ctf1_motd=$ctf1/motd


msg() {
    echo '[*]' $*
}

cmd() {
    echo '[cmd]' $*
    $*
}

error() {
    echo '[E]' $*
    exit 1
}

exit_if_nonroot() {
    test $(id -u) = 0 || error this script needs to run as root
}

get_tcz() {
    mkdir -pv $tcz_dir
    for package; do
        target=$tcz_dir/$package.tcz
        test -f $target || curl -o $target $tcz_url/$package.tcz
    done
    rmdir -pv $tcz_dir 2>/dev/null
}

install_tcz() {
    get_tcz $@
    for package; do
        target=$tcz_dir/$package.tcz
        tce_marker=$extract/usr/local/tce.installed/$package
        if ! test -f $tce_marker; then
            unsquashfs -f -d $extract $target
            touch $tce_marker
        fi
    done
}

for i in "$@"; do
    case "$i" in
        -h|--help) usage ; exit 1 ;;
    esac
done

# eof
