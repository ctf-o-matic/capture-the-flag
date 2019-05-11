Some levels require setuid root privileges to be vulnerable,
however, even if a setuid program can be tricked to executing
external programs like /bin/cat, normally it doesn't work.
For example the system() call executes programs with:

    /bin/sh -c prog

However, /bin/sh in TinyCore is busybox ash, and it drops
setuid privileges. To circumvent this, we modified the
original contest source codes by inserting this:

    // circumvent busybox ash dropping privileges
    uid_t uid = geteuid();
    setreuid(uid, uid);

A nice side effect of this is that this breaks the
published solutions circulated on the internet,
making it a little bit more difficult to cheat.
