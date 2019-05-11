#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

exit_if_nonroot

# install software
./scripts/install-python.sh   # required by contest
install_tcz curl      # hacking tool
install_tcz binutils  # hacking tool
install_tcz gdb       # hacking tool
install_tcz ruby      # hacking tool
install_tcz nano || : # easier editor than vi...
install_tcz kmaps     # for international use
./scripts/install-openssh.sh  # just for convenience

# copy original source codes to work
work_code=$work_ctf1/code/levels
mkdir -p $work_code
rsync -rv $ctf1_code/levels/level* $work_code/

work_special=$work_ctf1/special/levels
mkdir -p $work_special
rsync -rv $ctf1_special/levels/level* $work_special/

# build programs for i686
for i in $work_code/level*; do
    test -f $i/Makefile && (cd $i; $as_user make CFLAGS="-m32")
done

# build extra programs
for i in $work_special/level*; do
    test -f $i/Makefile && (cd $i; $as_user make CFLAGS="-m32")
done

# create users
create_users0=/tmp/create-users.sh
create_users=$extract$create_users0
for i in 0 1 2 3 4 5 6; do
    pass=$(pwgen 8 1)
    echo "# level0$i"
    echo "adduser -s /bin/sh -u 110$i -D level0$i"
    echo "echo level0$i:$pass | chpasswd --md5"
    echo "echo $pass > /home/level0$i/.password"
    echo
done | tee $create_users

# add users to groups
for i in 0 1 2 3 4 5; do
    echo "addgroup level0$i level0$((i+1))"
done | tee -a $create_users

# run create user script in chroot
chmod 755 $create_users
chroot $extract $create_users0
rm $create_users

# copy ctf1 files
mkdir -p $extract/levels/level00
rsync -rv $ctf1_append/* $extract/

# copy ctf1 code
rsync -rv $work_code/ $extract/levels
#rsync -rv $work_special/ $extract/levels --exclude '*.c'
rsync -rv $work_special/ $extract/levels

# fix permissions
chmod -R go-w $extract/home/level0?
chmod -R go-rx $extract/home/level0[1-9]
chmod -R g-s $extract/home/level0?
chmod 0750 $extract/levels/level0?

# fix ownerships
chown -R 0.50 $extract/root
chown 0.50 $extract/levels

# create message files
for i in 0 1 2 3 4 5 6; do
    cat $ctf1_motd/banner.txt $ctf1_motd/level0$i.txt > $extract/home/level0$i/motd.txt
    echo clear >> $extract/home/level0$i/.profile
    echo 'cat ~/motd.txt' >> $extract/home/level0$i/.profile
done

# fix ownerships
for i in 0 1 2 3 4 5 6; do
    chown -R 110$i.110$i $extract/home/level0$i
    chown -R 110$i.110$i $extract/levels/level0$i
    to_setuid=$extract/levels/level0$i/level0$i
    test -f $to_setuid && chmod 4755 $to_setuid
done

# customize boot screen
rsync -rv $ctf1/boot/ $newiso/boot

# eof
