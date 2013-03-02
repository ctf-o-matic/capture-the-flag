ctf-o-matic
===========
Remaster Linux Live CD images for the purpose of creating ready to
use hacking contests with pre-installed vulnerabilities to exploit.

**IMPORTANT: this is a work in progress**


Requirements
------------
You need the following to build the Live CD using the scripts
in this project.

* Linux, with root access
* `git`
* `make`
* `gcc`
* `pwgen`


How to use
----------
1. Download the smallest TinyCore Linux live cd image from: 
   http://distro.ibiblio.org/tinycorelinux/downloads.html

2. Copy or symlink the live cd image file to `livecd.iso`

3. Get the files of the first Capture The Flag contest from GitHub:

        ./scripts/get-ctf1.sh

4. Unpack the live cd image:

        sudo ./scripts/unpack-iso.sh
        # TODO: we should not need root here

5. Unpack the squashfs image inside the live cd

        sudo ./scripts/unpack-squashfs.sh
        # TODO: do we really need root here?

6. Setup the capture the flag challenges:

        sudo ./scripts/setup-ctf1.sh
        # TODO: do we really need root here?

7. Rebuild the iso:

        sudo ./scripts/repack.sh
        # TODO: do we really need root here?


Progress
--------
* Verified levels: 1, 3


Todo
----
* Use `sudo` *inside* the scripts, only when necessary, and eliminate
  all the `sudo` calls from the above steps (eliminating the TODOs above)

* Verify that levels 5, 6 work.

* Setup levels 2 and 4 (require web server)

* Add software inside the live cd:
    - ssh server
    - lighttpd
    - php
    - gdb
    - objdump
    - perl
    - python

* maybe: Generalize the scripts to use with other than TinyCore

* maybe: Implement the second Capture The Flag contest of Stripe


