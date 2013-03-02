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

# set a password for tc user
tcpass=$(pwgen 8 1)
echo "echo tc:$tcpass | chpasswd --md5" | tee -a $create_users
echo $tcpass | sudo tee $extract/home/tc/.password >/dev/null

# run create user script in chroot
chmod 755 $create_users
sudo chroot $extract $create_users0
sudo rm $create_users

# copy ctf1 files
sudo mkdir -p $extract/levels/level00
sudo rsync -av $ctf1/code/level0? $extract/levels/
sudo rsync -av $ctf1_extra/* $extract/ --exclude level01.c --exclude level03.c

# fix permissions
sudo chmod 0750 $extract/home/level0?
sudo chmod g-s $extract/home/level0?
sudo chmod 0400 $extract/home/level0?/.password
sudo chmod 0750 $extract/levels/level0?

# create message files
for i in 0 1 2 3 4 5 6; do
    cat $ctf1_extra/motd/banner.txt $ctf1_extra/motd/level0$i.txt | sudo tee $extract/home/level0$i/motd.txt >/dev/null
    printf 'clear\ncat ~/motd.txt\n' | sudo tee -a $extract/home/level0$i/.profile >/dev/null
done

# fix ownerships
for i in 0 1 2 3 4 5 6; do
    sudo chown -R 110$i.110$i $extract/home/level0$i
    sudo chown -R 110$i.110$i $extract/levels/level0$i
    sudo chmod 4755 $extract/levels/level0$i/level0$i || :
done

# eof
