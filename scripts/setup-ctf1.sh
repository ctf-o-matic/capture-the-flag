#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

# build programs
for i in $ctf1/code/level*; do
    test -f $i/Makefile && (cd $i; make)
done

# build extra programs
for i in $ctf1_extra/levels/level*; do
    test -f $i/Makefile && (cd $i; make)
done

# create users
create_users0=/tmp/create-users.sh
create_users=$extract$create_users0
for i in 1 2 3 4 5 6; do
    pass=$(pwgen 8 1)
    echo "# level0$i"
    echo "adduser -s /bin/sh -u 110$i -D level0$i"
    echo "echo level0$i:$pass | chpasswd --md5"
    echo "echo $pass > /home/level0$i/.password"
    echo
done | tee $create_users

# add users to groups
for i in 1 2 3 4 5 6; do
    test $i = 1 && user=tc || user=level0$((i-1))
    echo "addgroup $user level0$i"
done | tee -a $create_users

# run create user script in chroot
chmod 755 $create_users
sudo chroot $extract $create_users0
sudo rm $create_users

# copy ctf1 files
sudo mkdir $extract/levels
sudo rsync -av $ctf1/code/level0? $extract/levels/
sudo rsync -av $ctf1_extra/* $extract/ --exclude level01.c --exclude level03.c

# fix permissions
sudo chmod 0750 $extract/home/level0?
sudo chmod g-s $extract/home/level0?
sudo chmod 0400 $extract/home/level0?/.password
sudo chmod 0750 $extract/levels/level0?

for i in 1 2 3 4 5 6; do
    sudo chown -R 110$i.110$i $extract/home/level0$i
    sudo chown -R 110$i.110$i $extract/levels/level0$i
    sudo chmod 4755 $extract/levels/level0$i/level0$i
done

# eof
