#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

cat<<EOF >/dev/null
if ! ls $squashfs >/dev/null 2>/dev/null; then
    mount | grep $livecd0 >/dev/null || cmd sudo mount $livecd0 $mnt
    cmd mkdir -p $newiso
    cmd rsync -av $mnt/* $newiso/
    cmd sudo umount $livecd0
fi
EOF

for i in $ctf1/code/level*; do
    test -f $i/Makefile && (cd $i; make)
    chmod -v u+s $i/level??
done

create_users0=/tmp/create-users.sh
create_users=$extract$create_users0
for i in 1 2 3 4 5 6; do
    pass=pass$i
    echo "# level0$i"
    echo "adduser -s /bin/sh -u 110$i -D level0$i"
    echo "echo level0$i:$pass | chpasswd --md5"
    echo "echo $pass > /home/level0$i/.password"
    echo
done | tee $create_users

cat<<EOF | tee -a $create_users
chmod g-s /home/level0?
chmod 400 /home/level0?/.password

EOF

chmod 755 $create_users
sudo chroot $extract $create_users0
sudo rm $create_users

sudo rsync -av $ctf1/code/level0? $extract/home/

for i in 1 2 3 4 5 6; do
    sudo chown -R 110$i.110$i $extract/home/level0$i
    j=$((i+1))
    sudo chown 110$j.110$j $extract/home/level0$i/level0$i
    sudo chmod u+s $extract/home/level0$i/level0$i
done

# eof
