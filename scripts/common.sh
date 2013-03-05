#!/bin/sh
#
# File: common.sh
# Purpose: common configuration and shell functions
#

# tiny core related
# http://distro.ibiblio.org/tinycorelinux/downloads.html
livecd_url=http://distro.ibiblio.org/tinycorelinux/4.x/x86/release/Core-current.iso
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
ctf1_code=$ctf1/code
ctf1_append=$ctf1/append
ctf1_motd=$ctf1/motd

test "$SUDO_USER" && runas="sudo -u $SUDO_USER" || runas=


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
        if test ! -f $target; then
            msg fetching package $package ...
            $runas curl -o $target $tcz_url/$package.tcz
        fi
        dep=$target.dep
        if test ! -f $dep; then
            msg fetching dep list of $package ...
            $runas curl -o $dep $tcz_url/$package.tcz.dep || touch $dep
            grep -q 404 $dep && >$dep
            if test -s $dep; then
                get_tcz $(sed -e s/.tcz$// $dep)
            fi
        fi
    done
}

install_tcz() {
    get_tcz $@
    exit_if_nonroot
    for package; do
        target=$tcz_dir/$package.tcz
        tce_marker=$extract/usr/local/tce.installed/$package
        if ! test -f $tce_marker; then
            msg installing package $package ...
            unsquashfs -f -d $extract $target
            if test -s $tce_marker; then
                chroot $extract /usr/local/tce.installed/$package
            else
                touch $tce_marker
            fi
        fi
        dep=$target.dep
        if test -s $dep; then
            install_tcz $(sed -e s/.tcz$// $dep)
        fi
    done
}


for i in "$@"; do
    case "$i" in
        -h|--help) usage ; exit 1 ;;
    esac
done

# eof
